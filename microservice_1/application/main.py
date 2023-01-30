from prometheus_api_client import PrometheusConnect, MetricRangeDataFrame
from prometheus_api_client.utils import parse_datetime
from statsmodels.graphics.tsaplots import acf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from MessageProducer import MessageProducerClass
from LogMonitor import LogMonitorClass
from threading import Thread
from datetime import timedelta
from time import sleep, time
import json
import os
import grpc
import sys
sys.path.append('./gRPCUtils')

import echo_pb2
import echo_pb2_grpc
from MetricCalculator import MetricCalculator
from multiprocessing import Process, SimpleQueue
from gRPCServer import serve


""" Main Function """

def main(queue_metrics, queue_predictions, message_producer):

    try:
        file = open("../config.json", "r")
    except FileNotFoundError:
        print("File not found.")

    data = json.load(file) 
    file.close()
    
    insert_stats_on_data_storage(data['stats'])
    insert_metrics_on_data_storage(data['metrics'])
    
    #Creo un topic con tante partizioni tante quante sono le metriche
    message_producer.create_topic(len(data['metrics']))

    prom = PrometheusConnect(url=os.environ['PROMETHEUS_SERVER'], disable_ssl=True)
    """ Start metadata calculus """
    init_time = time()
    queryResult = prom.custom_query(query='{job="' + data['job'] +'"}[' + data['range_time'] +']')
    time_query_delay = time() - init_time

    for metricResultQuery in queryResult:
        for metric in data['metrics']:
            if metricResultQuery['metric']['__name__'] == metric['name']:
                if is_subset( metric['labels'], metricResultQuery['metric']):
                    init_monitoring_time = time() - time_query_delay
                    metric_values = MetricRangeDataFrame(metricResultQuery)
                    thread_metadata = Thread(target=calculate_metadata_values, args=(init_monitoring_time, metricResultQuery['metric'], metric_values['value'], data['metrics'].index(metric)))
                    thread_metadata.start()
                    break
    sleep_time = 600
    if os.environ.get('INTERVAL_TIME_SECONDS'):
        sleep_time = int(os.environ['INTERVAL_TIME_SECONDS'])

    interval_time_list = ['1h', '3h', '12h']
    MetricCalculator.interval_time_list = interval_time_list

    """ Start statistics and predictions calculus """
    while True:
        d = { '1h': list(), '3h': list(), '12h': list() }
        data_predictions = []

        for metric in data['metrics']:
            for interval_time in interval_time_list:
                
                init_monitoring_time = time()
                start_time = parse_datetime(interval_time)
                end_time = parse_datetime("now")
                chunk_size = timedelta(minutes=5)

                metric_data = prom.get_metric_range_data(
                    metric_name=metric['name'],
                    label_config=metric['labels'],
                    start_time=start_time,
                    end_time=end_time,
                    chunk_size=chunk_size,
                )
                metric_dataframe = MetricRangeDataFrame(metric_data)
                d[interval_time].append({"__name__": metric['name'], 'values': metric_dataframe['value'].tolist()})

                thread_stats = Thread(target=calculate_stats_values, args=(init_monitoring_time, metric, metric_dataframe, interval_time, data['metrics'].index(metric)))
                thread_stats.start()
                
                # Per la predizione programmaticamente utilizzo l'intervallo di tempo più lungo che ho (l'ultimo della lista).
                if interval_time == interval_time_list[-1]:
                    predictions = calculate_prediction_values(init_monitoring_time, metric, metric_dataframe, queue_predictions, data['metrics'].index(metric))
                    data_predictions.append(predictions)
        
        #Inserisco nelle code le metriche e le predizioni che utilizzerà il gRPC server
        print("METRICHE " + str(d))
        queue_metrics.put(str(d))
        print("Predizioni " + str(data_predictions))
        queue_predictions.put(str(data_predictions))
        print("go to sleep")
        sleep(sleep_time)

""" Functions """

def is_subset(a, b):
    subset = {}
    for k, v in a.items():
        if k in b:
            subset[k] = b[k]
    return subset == a

def insert_stats_on_data_storage(metrics) :
    print("Waiting grpc server")
    sleep(20.0)
    while True :
        with grpc.insecure_channel('microservice_2:50051') as channel:
            stub = echo_pb2_grpc.EchoServiceStub(channel)
            print("send value")
            query_result = stub.sendStats(echo_pb2.statsNameParam(statsName=json.dumps(metrics)))
            if query_result.result == 'True' :
                break
    print("exit from while")

def insert_metrics_on_data_storage(metrics) :
    print("Waiting grpc server")
    metric_to_insert = list()
    for metric in metrics :
        metric_to_insert.append(metric['name'])
    while True :
        with grpc.insecure_channel('microservice_2:50051') as channel:
            stub = echo_pb2_grpc.EchoServiceStub(channel)
            print("send value")
            query_result = stub.sendMetrics(echo_pb2.statsNameParam(statsName=json.dumps(metric_to_insert)))
            if query_result.result == 'True' :
                break
    print("exit from while")


""" Metadata calculus """
def calculate_metadata_values(init_monitoring_time, metric_info, values, offset_partition):

    """ Autocorrelazione """
    acf_result_values = acf(values)
    acf_result = 0
    for val in acf_result_values:
        acf_result += val

    autocorrelation = "Errore calcolo autocorrelazione"
    if acf_result > 0.6 and acf_result < 1:
        autocorrelation = 'Serie con correlazione positiva'
    elif acf_result > 0.2 and acf_result < 0.6:
        autocorrelation = 'Serie scarsamente correlata positivamente'
    elif acf_result > -0.2 and acf_result < 0.2:
        autocorrelation = 'Serie con correlazione nulla'
    elif acf_result > -0.6 and acf_result < -0.2:
        autocorrelation = 'Serie scarsamente correlata negativamente'
    elif acf_result > -1 and acf_result < -0.6:
        autocorrelation = 'Serie con correlazione negativa'

    """ Stazionarietà """
    stationarity_test = adfuller(values, autolag='AIC')
    stationarity = 'false'
    if stationarity_test[1] <= 0.05:
        print(metric_info['__name__'] + ' is stationary')
        stationarity = 'true'

    """ Stagionalità """
    seasonability = seasonal_decompose(values, model='additive', period=10)
    season_list = seasonability.seasonal.tolist()
    seasonality = json.dumps(season_list[0:120])

    """ Write Log """
    log_time_seconds = time() - init_monitoring_time
    message = 'Metadata - Metric ' + metric_info['__name__'] + ' took ' + str(round(log_time_seconds)) + ' sec to elaborate data'
    log_monitor.write_log_monitoring(message)

    data = {
        'name': metric_info['__name__'],
        'type': 'metadata',
        'values': [
            {
                'name': 'autocorrelazione',
                'value': autocorrelation
            },
            {
                'name': 'stazionarieta',
                'value': stationarity
            },
            {
                'name': 'stagionalita',
                'value': seasonality
            },
        ]
    }

    message_producer.send_msg(data, offset_partition) #inviare alla partizione corretta dato l'indice del file di config

""" Statistics calculus """
def calculate_stats_values(init_monitoring_time, metric, metric_dataframe, interval_time, offset_partition):

    max = round(metric_dataframe['value'].max())
    min = round(metric_dataframe['value'].min())
    avg = round(metric_dataframe['value'].mean())
    dev_std = round(metric_dataframe['value'].std())

    """ Write Log """
    log_time_seconds = time() - init_monitoring_time
    message = 'Statistics ' + interval_time + ' - Metric ' + metric['name'] + ' took ' + str(round(log_time_seconds)) + ' sec to elaborate data'
    log_monitor.write_log_monitoring(message)

    data = {
        'name': metric['name'],
        'type': 'statistics',
        'values': {
            'time': interval_time,
            'stats': [
                {
                    'name': 'MAX',
                    'value': max
                },
                {
                    'name': 'MIN',
                    'value': min
                },
                {
                    'name': 'AVG',
                    'value': avg
                },
                {
                    'name': 'DEV_STD',
                    'value': dev_std
                }
            ]
        }
    }

    message_producer.send_msg(data, offset_partition) #inviare alla partizione corretta dato l'indice del file di config


""" Predictions calculus """
def calculate_prediction_values(init_monitoring_time, metric, metric_dataframe, queue_predictions, offset_partition):

    resampled_data = metric_dataframe['value'].resample(rule='1T')
    max = resampled_data.max()
    min = resampled_data.min()
    avg = resampled_data.mean()

    prediction_max = ExponentialSmoothing(max, trend='add', seasonal='add',seasonal_periods=10).fit()
    prediction_min = ExponentialSmoothing(min, trend='add', seasonal='add',seasonal_periods=10).fit()
    prediction_avg = ExponentialSmoothing(avg, trend='add', seasonal='add',seasonal_periods=10).fit() 

    result_max = prediction_max.forecast(10).to_dict()
    result_min = prediction_min.forecast(10).to_dict()
    result_avg = prediction_avg.forecast(10).to_dict()

    list_max = []
    list_max_prediction = []
    list_min = []
    list_min_prediction = []
    list_avg = []
    list_avg_prediction = []
    for key, value in result_max.items():
        list_max.append((str(key), str(value)))
        list_max_prediction.append(str(value))
    for key, value in result_min.items():
        list_min.append((str(key), str(value)))
        list_min_prediction.append(str(value))
    for key, value in result_avg.items():
        list_avg.append((str(key), str(value)))

    """ Write Log """
    log_time_seconds = time() - init_monitoring_time
    message = 'Predictions - Metric ' + metric['name'] + ' took ' + str(round(log_time_seconds)) + ' sec to elaborate data'
    log_monitor.write_log_monitoring(message)

    data = {
        'name': metric['name'],
        'type': 'prediction',
        'values': [
            {
                'name': 'MAX',
                'value': json.dumps(list_max)
            },
            {
                'name': 'MIN',
                'value': json.dumps(list_min)
            },
            {
                'name': 'AVG',
                'value': json.dumps(list_avg)
            }
        ]
    }

    data_for_calculator = {
        'name': metric['name'],
        'type': 'prediction',
        'values': [
            {
                'name': 'MAX',
                'value': list_max_prediction
            },
            {
                'name': 'MIN',
                'value': list_min_prediction
            }
        ]
    }
    message_producer.send_msg(data, offset_partition)
    return data_for_calculator

""" Start Main Script """

if __name__ == '__main__':
    broker = os.environ['KAFKA_BROKER']
    topic = os.environ['KAFKA_TOPIC']
    message_producer = MessageProducerClass(broker, topic)
    #Queue che conterrà le metriche, permette la comunicazione tra questo processo ed il processo gRPC
    queue_metrics = SimpleQueue()
    #Queue che conterrà le predizioni, permette la comunicazione tra questo processo ed il processo gRPC
    queue_predictions = SimpleQueue()
    log_monitor = LogMonitorClass()
    p = Process(target=serve, args=[queue_metrics, queue_predictions])
    p.start()
    main(queue_metrics, queue_predictions, message_producer)

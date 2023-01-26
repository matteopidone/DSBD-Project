from prometheus_api_client import PrometheusConnect, MetricRangeDataFrame
from prometheus_api_client.utils import parse_datetime
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from MessageProducer import MessageProducerClass
from threading import Thread
from datetime import timedelta
from time import sleep, time
import json
import os

""" Main Function """

def main():

    try:
        file = open("../config.json", "r")
    except FileNotFoundError:
        print("File not found.")

    data = json.load(file) 
    file.close()

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
                    thread_metadata = Thread(target=calculate_metadata_values, args=(init_monitoring_time, metricResultQuery['metric'], metricResultQuery['values']))
                    thread_metadata.start()
                    break

    sleep_time = 600
    if os.environ.get('INTERVAL_TIME_SECONDS'):
        sleep_time = os.environ['INTERVAL_TIME_SECONDS']

    time_list = ['1h', '3h', '12h']

    """ Start statistics and predictions calculus """
    while True:
        for metric in data['metrics']:
            for time in time_list:
                
                init_monitoring_time = time()
                start_time = parse_datetime(time)
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

                thread_stats = Thread(target=calculate_stats_values, args=(init_monitoring_time, metric, metric_dataframe, time))
                thread_stats.start()
                thread_prediction = Thread(target=calculate_prediction_values, args=(init_monitoring_time, metric, metric_dataframe))
                thread_prediction.start()

        sleep(sleep_time)

""" Functions """

def is_subset(a, b):
    subset = {}
    for k, v in a.items():
        if k in b:
            subset[k] = b[k]
    return subset == a

""" Metadata calculus """
def calculate_metadata_values(init_monitoring_time, metric_info, values):

    log_time_seconds = time() - init_monitoring_time
    write_monitoring_log(log_time_seconds)

    data = {
        'name': metric_info['__name__'],
        'type': 'metadata',
        'values': {
            'autocorrelazione': 1,
            'stazionarieta': 4,
            'stagionalita': 8
        }
    }

    message_producer.send_msg(data)

""" Statistics calculus """
def calculate_stats_values(init_monitoring_time, metric, metric_dataframe, time):

    max = round(metric_dataframe['value'].max())
    min = round(metric_dataframe['value'].min())
    avg = round(metric_dataframe['value'].mean())
    dev_std = round(metric_dataframe['value'].std())

    log_time_seconds = time() - init_monitoring_time
    write_monitoring_log(log_time_seconds)

    data = {
        'name': metric['name'],
        'type': 'statistics',
        'values': {
            'time': time,
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

    message_producer.send_msg(data)

""" Predictions calculus """
def calculate_prediction_values(init_monitoring_time, metric, metric_dataframe):

    resampled_data = metric_dataframe['value'].resample(rule='1T')

    avg = resampled_data.mean()
    max = resampled_data.max()
    min = resampled_data.min()

    prediction_max = ExponentialSmoothing(max, trend='add', seasonal='add',seasonal_periods=4).fit()
    prediction_min = ExponentialSmoothing(min, trend='add', seasonal='add',seasonal_periods=4).fit()
    prediction_avg = ExponentialSmoothing(avg, trend='add', seasonal='add',seasonal_periods=4).fit() 

    result_max = prediction_max.forecast(10)
    result_min = prediction_min.forecast(10)
    result_avg = prediction_avg.forecast(10)

    log_time_seconds = time() - init_monitoring_time
    write_monitoring_log(log_time_seconds)

    data = {
        'name': metric['name'],
        'type': 'prediction',
        'values': {
            'max': max,
            'min': min,
            'avg': avg
        }
    }

    message_producer.send_msg(data)

""" Write log """
def write_monitoring_log(log_time_seconds):
    pass

""" Start Main Script """

if __name__ == '__main__':
    broker = os.environ['KAFKA_BROKER']
    topic = os.environ['KAFKA_TOPIC']
    message_producer = MessageProducerClass(broker, topic)
    main()

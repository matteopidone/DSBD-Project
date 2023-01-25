from prometheus_api_client import PrometheusConnect, MetricRangeDataFrame
from prometheus_api_client.utils import parse_datetime
from MessageProducer import MessageProducerClass
from threading import Thread
from datetime import timedelta
from time import sleep
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
    queryResult = prom.custom_query(query='{job="' + data['job'] +'"}[' + data['range_time'] +']')

    for metricResultQuery in queryResult:
        for metric in data['metrics']:
            if metricResultQuery['metric']['__name__'] == metric['name']:
                if is_subset( metric['labels'], metricResultQuery['metric']):
                    thread_metadata = Thread(target=calculate_metadata_values, args=(metricResultQuery['metric'], metricResultQuery['values']))
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
                thread_stats = Thread(target=calculate_stats_values, args=(prom, metric, time))
                thread_stats.start()
                thread_prediction = Thread(target=calculate_prediction_values, args=(prom, metric, time))
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
def calculate_metadata_values(metric_info, values):

    data = {
        'name': 'pippo',
        #labels
        'autocorrelazione': 1,
        'stazionarieta': 4,
        'stagionalita': 8
    }
    resp = message_producer.send_msg(data)

""" Statistics calculus """
def calculate_stats_values(prom, metric, time):

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
    max = round(metric_dataframe['value'].max())
    min = round(metric_dataframe['value'].min())
    avg = round(metric_dataframe['value'].mean())
    dev_std = round(metric_dataframe['value'].std())

    data = {
        'name': metric['name'],
        'type': 'statistics',
        'values': {
            'time': time,
            'max': max,
            'min': min,
            'avg': avg,
            'dev_std': dev_std
        }
    }

    resp = message_producer.send_msg(data)

""" Predictions calculus """
def calculate_prediction_values(prom, metric, time):
    #Calcoli
    #Record Key Prediction#indice_metrica
    data = {
        'name': 'pippo',
        'max': 10,
        'min': 1,
        'avg': 7,
    }
    resp = message_producer.send_msg(data)

""" Start Main Script """

if __name__ == '__main__':
    broker = os.environ['KAFKA_BROKER']
    topic = os.environ['KAFKA_TOPIC']
    message_producer = MessageProducerClass(broker, topic)
    main()

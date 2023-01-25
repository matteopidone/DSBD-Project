from prometheus_api_client import PrometheusConnect
from MessageProducer import MessageProducerClass
from threading import Thread
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
                    t0 = Thread(target=calculate_metadata_values, args=(metricResultQuery['metric'], metricResultQuery['values']))
                    t0.start()
                    break

    sleep_time = 600
    if os.environ.get('INTERVAL_TIME_SECONDS'):
        sleep_time = os.environ['INTERVAL_TIME_SECONDS']

    """ Start statistics and predictions calculus """
    while True:
        for metric in data['metrics']:

            t1 = Thread(target=calculate_stats_values, args=(prom, metric, '1h'))
            t2 = Thread(target=calculate_stats_values, args=(prom, metric, '3h'))
            t3 = Thread(target=calculate_stats_values, args=(prom, metric, '12h'))
            t1.start()
            t2.start()
            t3.start()
            t4 = Thread(target=calculate_prediction_values, args=(prom, metric, '1h'))
            t5 = Thread(target=calculate_prediction_values, args=(prom, metric, '3h'))
            t6 = Thread(target=calculate_prediction_values, args=(prom, metric, '12h'))
            t4.start()
            t5.start()
            t6.start()

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
        'autocorrelazione': 1,
        'stazionarieta': 4,
        'stagionalita': 8
    }
    resp = message_producer.send_msg(data)

""" Statistics calculus """
def calculate_stats_values(prom, metric, hours='1h'):
    print('inside calculate_stats_values')
    print(metric)
    
    #queryResult = prom.custom_query(query='{job="' + data['job'] +'"}[' + data['range_time'] +']')



    max = min = avg = dev_std = sum = n = 0

    for timestamp, value in metric:
        if value > max:
            max = value
        elif value < min:
            min = value
        sum += value
        n += 1

    avg = sum/n

    #Calcoli
    #Record Key Stats#indice_metrica
    data = {
        'name': 'pippo',
        'max': 10,
        'min': 1,
        'avg': 7,
        'dev_std': 2
    }
    resp = message_producer.send_msg(data)

""" Predictions calculus """
def calculate_prediction_values(prom, metric, hours='1h'):
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

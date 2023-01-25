from prometheus_api_client import PrometheusConnect
from MessageProducer import MessageProducerClass
from threading import Thread
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

    metrics_list = list()
    prom = PrometheusConnect(url=os.environ['PROMETHEUS_SERVER'], disable_ssl=True)
    queryResult = prom.custom_query(query='{job="' + data['job'] +'"}[' + data['range_time'] +']')

    for metricResultQuery in queryResult:
        for metric in data['metrics']:
            if metricResultQuery['metric']['__name__'] == metric['name']:
                if is_subset( metric['labels'], metricResultQuery['metric']):
                    t1 = Thread(target=calculate_stats_values, args=(metricResultQuery,))
                    t2 = Thread(target=calculate_prediction_values, args=(metricResultQuery,))
                    t3 = Thread(target=calculate_metadata_values, args=(metricResultQuery,))
                    t1.start()
                    t2.start()
                    t3.start()
                    t1.join()
                    t2.join()
                    t3.join()
                    break

""" Functions """

def is_subset(a, b):
    subset = {}
    for k, v in a.items():
        if k in b:
            subset[k] = b[k]
    return subset == a

def calculate_stats_values(metric, hours='1h'):
    print('inside calculate_stats_values')
    print(metric)
    
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
    print(resp)
    return resp

def calculate_metadata_values(metric, hours='1h'):
    #Calcoli
    #Record Key Metadata#indice_metrica
    data = {
        'name': 'pippo',
        'autocorrelazione': 1,
        'stazionarieta': 4,
        'stagionalita': 8
    }
    resp = message_producer.send_msg(data)
    print(resp)
    return resp

def calculate_prediction_values(metric, hours='1h'):
    #Calcoli
    #Record Key Prediction#indice_metrica
    data = {
        'name': 'pippo',
        'max': 10,
        'min': 1,
        'avg': 7,
    }
    resp = message_producer.send_msg(data)
    print(resp)
    return resp

""" Start Main Script """

if __name__ == '__main__':
    broker = "kafka:9092"
    topic = "prova"
    message_producer = MessageProducerClass(broker, topic)
    main()

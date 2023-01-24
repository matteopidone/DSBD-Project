from prometheus_api_client import PrometheusConnect, MetricsList, MetricSnapshotDataFrame, MetricRangeDataFrame
from datetime import timedelta
from prometheus_api_client.utils import parse_datetime
import sys
import json
from MessageProducer import MessageProducerClass
from threading import Thread

""" Main Function """

def main():
    # try and catch da inserire
    file = open("../config.json")
    data = json.load(file)
    file.close()

    metrics_list = list()
    prom = PrometheusConnect(url="http://15.160.61.227:29090/", disable_ssl=True) # togliere l'url e metterlo in env
    queryResult = prom.custom_query(query='{job="' + data['job'] +'"}[' + data['range_time'] +']')

    for metricResultQuery in queryResult :
        for metric in data['metrics']:
            if metricResultQuery['metric']['__name__'] == metric['name']:
                if( is_subset( metric['labels'], metricResultQuery['metric'] ) ):
                    #metriche desiderate
                    t1 = Thread(target=calculate_stats_values, args=(metricResultQuery,))
                    t1.start()
                    t2 = Thread(target=calculate_prediction_values(metrics_list), args=(metricResultQuery,))
                    t2.start()
                    t3 = Thread(target=calculate_metadata_values(metrics_list), args=(metricResultQuery,))
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
    #Calcoli
    #Record Key Stats#indice_metrica
    data = {
        'name': 'pippo',
        'max': 10,
        'min': 1,
        'avg': 7
    }
    resp = message_producer.send_msg(data)
    print(resp)
    return resp

def calculate_metadata_values(metric, hours='1h'):
    #Calcoli
    #Record Key Metadata#indice_metrica
    data = {
        'name': 'pippo',
        'dev_std': 10,
        'autocorrelazione': 1
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
        'dev_std': 4
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

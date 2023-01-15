from prometheus_api_client import PrometheusConnect, MetricsList, MetricSnapshotDataFrame, MetricRangeDataFrame
from datetime import timedelta
from prometheus_api_client.utils import parse_datetime
from confluent_kafka import Producer
import sys
import json

def is_subset(a, b):
    subset = {}
    for k, v in a.items():
        if k in b:
            subset[k] = b[k]
    return subset == a

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
                metrics_list.append(metricResultQuery)
                break
print(metrics_list)
maxx = 10
minn = 2
dev_std = 150

#calcolo stagionalità, min, max

#invio topic kafka
broker = "localhost:/9092"
topic = "prometheusdata"
conf = {'bootstrap.servers': broker}

p = Producer(**conf)

def delivery_callback(err, msg):
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('%% Message delivered to %s, partition[%d] @ %d\n' %
                            (msg.topic(), msg.partition(), msg.offset()))

try:
    record_key = "Prod#1"
    record_value = json.dumps({'count': '1'})
    print("Producing record: {}\t{}".format(record_key, record_value))
    p.produce(topic, key=record_key, value=record_value, callback=delivery_callback)

except BufferError:
    sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                        len(p))

# Serve delivery callback queue.
# NOTE: Since produce() is an asynchronous API this poll() call
#       will most likely not serve the delivery callback for the
#       last produce()d message.
p.poll(0)

# Wait until all messages have been delivered
sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
p.flush()
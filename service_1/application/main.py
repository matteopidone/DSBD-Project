from prometheus_api_client import PrometheusConnect, MetricsList, MetricSnapshotDataFrame, MetricRangeDataFrame
from datetime import timedelta
from prometheus_api_client.utils import parse_datetime

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
queryResult = prom.custom_query(query='{job="' + data['job_name'] +'"}[' + data['range_time'] +']')

for metric_info in queryResult :
    for metrics in data['metrics']:
        if metric_info['metric']['__name__'] == metrics['metric_name']:
            if( is_subset( metrics['metadata'], metric_info['metric'] ) ):
                #metriche desiderate
                metrics_list.append(metric_info)
print(metrics_list)
maxx = 10
minn = 2
dev_std = 150

#calcolo staginalità, min, max

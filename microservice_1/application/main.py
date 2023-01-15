from prometheus_api_client import PrometheusConnect, MetricsList, MetricSnapshotDataFrame, MetricRangeDataFrame
from datetime import timedelta
from prometheus_api_client.utils import parse_datetime

import json

# try and catch da inserire

file = open("../config.json")
data = json.load(file)
file.close()

metrics_list = list()
prom = PrometheusConnect(url="http://15.160.61.227:29090/", disable_ssl=True) # togliere l'url e metterlo in env
queryResult = prom.get_current_metric_value(label_config={'job' : data['job_name']})

for metric_info in queryResult :
    if metric_info['metric']['__name__'] == data['job_name']['metric_name'] :
        print(metric_info['metric']['__name__'])

#metric_df = MetricSnapshotDataFrame(queryResult)
#print(metric_df)
#print(metric_df["__name__"][1])
#print(metric_df["timestamp"][1])
#print(metric_df["value"][1])
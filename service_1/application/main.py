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
queryResult = prom.custom_query(query='{job="' + data['job_name'] +'"}')

for metric_info in queryResult :
    for metrics in data['metrics']:
        if metric_info['metric']['__name__'] == metrics['metric_name']:
            metric_info_json = json.loads(metric_info)
            print(metric_info_json)

#metric_df = MetricSnapshotDataFrame(queryResult)
#print(metric_df)
#print(metric_df["__name__"][1])
#print(metric_df["timestamp"][1])
#print(metric_df["value"][1])
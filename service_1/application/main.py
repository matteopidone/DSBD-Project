print("Service_1")
print("Before import libraries")

from prometheus_api_client import PrometheusConnect, MetricsList, MetricSnapshotDataFrame, MetricRangeDataFrame
from datetime import timedelta
from prometheus_api_client.utils import parse_datetime

print("Starting script")
prom = PrometheusConnect(url="http://15.160.61.227:29090/", disable_ssl=True)
label_config = {'job': 'summary'}
queryResult = prom.get_current_metric_value(metric_name='availableMem', label_config=label_config)
metric_df = MetricSnapshotDataFrame(queryResult)
print(metric_df)
print(metric_df["__name__"][1])
print(metric_df["timestamp"][1])
print(metric_df["value"][1])
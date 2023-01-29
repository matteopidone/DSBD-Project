import grpc
import sys
sys.path.append('./gRPCUtils')
import echo_pb2
import echo_pb2_grpc
from concurrent import futures
from Database import DataStorageDatabaseClass

class EchoService(echo_pb2_grpc.EchoServiceServicer):

    def getAllMetrics(self, request, context) :
        db_instance = DataStorageDatabaseClass()
        result = db_instance.get_all_metrics()
        return echo_pb2.resultValue(result=result)
    
    def getAllStatistics(self, request, context) :
        db_instance = DataStorageDatabaseClass()
        result = db_instance.get_all_statistics()
        return echo_pb2.resultValue(result=result)

    def getMetadataForMetrics(self, request, context) :
        db_instance = DataStorageDatabaseClass()
        result = db_instance.get_metadata_for_metrics(id_metric=request.idMetric)
        return echo_pb2.resultValue(result=result)

    def getHistoryForMetrics(self, request, context) :
        db_instance = DataStorageDatabaseClass()
        result = db_instance.get_history_for_metrics(id_metric=request.idMetric)
        return echo_pb2.resultValue(result=result)

    """ Function exposed to ETL Data Pipeline """

    def sendStats(self, request, context) :
        db_instance = DataStorageDatabaseClass()
        result = db_instance.insert_or_update_stats_conf(stats_list=request.statsName)
        return echo_pb2.resultValue(result=result)
    
    def sendMetrics(self, request, context) :
        db_instance = DataStorageDatabaseClass()
        result = db_instance.insert_or_update_metrics_conf(metric_list=request.statsName)
        return echo_pb2.resultValue(result=result)

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    echo_pb2_grpc.add_EchoServiceServicer_to_server(EchoService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Echo Service started, listening on " + port)
    server.wait_for_termination()
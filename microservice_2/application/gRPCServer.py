import grpc
import echo_pb2
import echo_pb2_grpc
from concurrent import futures
from connect_to_db import connect

class EchoService(echo_pb2_grpc.EchoServiceServicer):

    def getAllMetrics(self, request, context) :
        '''
        database = connect()
        cursor = database.cursor()
        try:
            cursor.execute("SELECT * FROM statistiche")
            query_result = cursor.fetchall()
            print('query result' + query_result)
            if query_result :
                return echo_pb2.AllMetrics(idMetric=query_result[0], metricName=query_result[1])
            else :
                return echo_pb2.AllMetrics(idMetric='', metricName='')
        except :
            print("Error while execute the query")
        finally:
            cursor.close()
            database.close()'''
        l = [(1, 'pippo'), (2, 'pluto')]
        return echo_pb2.AllMetrics(result=str(l).strip('[]'))


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    echo_pb2_grpc.add_EchoServiceServicer_to_server(EchoService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Echo Service started, listening on " + port)
    server.wait_for_termination()
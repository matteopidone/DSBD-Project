import grpc
import echo_pb2
import echo_pb2_grpc
from concurrent import futures
from connect_to_db import connect

class EchoService(echo_pb2_grpc.EchoServiceServicer):

    def getAllMetrics(self, request, context) :
        database = connect()
        cursor = database.cursor()
        try:
            cursor.execute("SELECT * FROM statistiche")
            query_result = cursor.fetchall()
            if query_result :
                return echo_pb2.AllMetrics(result=str(query_result).strip('[]'))
            else :
                return echo_pb2.AllMetrics(result=str())
        except :
            print("Error while execute the query")
        finally:
            cursor.close()
            database.close()
    
    def getMetadataForMetrics(self, request, context) :
        database = connect()
        cursor = database.cursor()
        try :
            cursor.execute("Select nome, metadata FROM metriche WHERE id = %s LIMIT 1", (request.idMetric,))
            query_result = cursor.fetchone()
            if query_result :
                return  echo_pb2.AllMetrics(result=str(query_result).strip('[]'))
            else :
                return echo_pb2.AllMetrics(result=str())
        except :
            print("Error while execute the query", e)
        finally:
            cursor.close()
            database.close()

    def getHistoryForMetrics(self, request, context) :
        database = connect()
        cursor = database.cursor()
        try:
            cursor.execute("SELECT metriche.nome, statistiche.nome, statistiche_metriche.1h, statistiche_metriche.3h, statistiche_metriche.12h FROM metriche JOIN statistiche_metriche ON metriche.id=statistiche_metriche.id_metrica JOIN statistiche on statistiche.id=statistiche_metriche.id_statistica WHERE metriche.id= %s", (request.idMetric,))
            query_result = cursor.fetchall()
            if query_result :
                return  echo_pb2.AllMetrics(result=str(query_result).strip('[]'))
            else :
                return echo_pb2.AllMetrics(result=str())
        except :
            print("Error while execute the query")
        finally:
            cursor.close()
            database.close()


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    echo_pb2_grpc.add_EchoServiceServicer_to_server(EchoService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Echo Service started, listening on " + port)
    server.wait_for_termination()
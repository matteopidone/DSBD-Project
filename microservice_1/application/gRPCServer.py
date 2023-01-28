import grpc
import sys
sys.path.append('./gRPCUtils')
import echo_pb2
import echo_pb2_grpc
import asyncio
from MetricCalculator import MetricCalculator

class EchoService(echo_pb2_grpc.EchoServiceServicer):

    def getNumberOfViolationsPast(self, request, context) :
        calculator_instance = MetricCalculator()
        result = calculator_instance.get_number_violation(request.listMetricsParam)
        
        return echo_pb2.resultValue(result=result)

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    echo_pb2_grpc.add_EchoServiceServicer_to_server(EchoService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Echo Service started, listening on " + port)
    server.wait_for_termination()
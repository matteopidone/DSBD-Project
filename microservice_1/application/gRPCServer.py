import grpc
import sys
sys.path.append('./gRPCUtils')
import echo_pb2
import echo_pb2_grpc
from concurrent import futures
from MetricCalculator import MetricCalculator

class EchoService(echo_pb2_grpc.EchoServiceServicer):
    queue = ''
    messagge = None
    def __init__(self, queue) :
        self.queue = queue
        super().__init__()
        ''' Message expected from Etl_Data_pipeline
        self.message = {
            '1h': [
                {
                '__name__': 'availableMem',
                'values': [12, 15,18]
                }
            ],
            '3h': [
                {
                '__name__': 'availableMem',
                'values': [12, 15, 18]
                }
            ],
            '12h': [
                {
                '__name__': 'availableMem',
                'values': [12, 15, 18]
                }
            ],
        }'''


    def getNumberOfViolationsPast(self, request, context) :
        ''' Gestire
        if (self.queue.empty() and self.messagge == None) :
            print("empty")
            return echo_pb2.resultValue(result='Error') 
        '''
        while not (self.queue.empty()) :
            self.message = self.queue.get()

        calculator_instance = MetricCalculator()
        result = calculator_instance.get_number_violation(request.listMetrics, str(self.message))
        
        return echo_pb2.resultValue(result=str(result))

def serve(s):
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    #Passo la Queue all'Echo Service per far comunicare i processi
    echo_pb2_grpc.add_EchoServiceServicer_to_server(EchoService(s), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Echo Service started, listening on " + port)
    server.wait_for_termination()
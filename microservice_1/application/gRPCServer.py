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
        self.message = ''
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
        while not (self.queue.empty()) :
            self.message = self.queue.get()

        #Se l'etl ha prodotto i dati calcolo le violazioni, altrimenti invio messaggio di errore
        if self.message :
            calculator_instance = MetricCalculator()
            result = calculator_instance.get_number_violation(request.listMetrics, str(self.message))
            print("Risultato " + str(result))
            return echo_pb2.resultValue(result=str(result))
        else : 
            return echo_pb2.resultValue(result='')

    def getNumberOfViolationsFuture(self, request, context) :
        while not (self.queue_prediction.empty()) :
            self.message_prediction = self.queue_prediction.get()

        #Se l'etl ha prodotto i dati calcolo le violazioni, altrimenti invio messaggio di errore
        if self.message_prediction :
            calculator_instance = MetricCalculator()
            result = calculator_instance.get_number_future_violation(request.listMetrics, str(self.message_future))
            print("Risultato " + str(result))
            return echo_pb2.resultValue(result=str(result))
        else : 
            return echo_pb2.resultValue(result='')
    
    
def serve(s):
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    #Passo la Queue all'Echo Service per far comunicare i processi
    echo_pb2_grpc.add_EchoServiceServicer_to_server(EchoService(s), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Echo Service started, listening on " + port)
    server.wait_for_termination()

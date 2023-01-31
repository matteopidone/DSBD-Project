import grpc
import sys
sys.path.append('./gRPCUtils')
import echo_pb2
import echo_pb2_grpc
from concurrent import futures
from MetricCalculator import MetricCalculator

class EchoService(echo_pb2_grpc.EchoServiceServicer):
    queue_metrics = ''
    queue_predictions = ''
    message = None
    message_predictions = None


    def __init__(self, queue_metrics, queue_predictions) :
        self.queue_metrics = queue_metrics
        self.queue_predictions = queue_predictions
        self.message = ''
        self.message_predictions = ''
        super().__init__()

    def getNumberOfViolationsPast(self, request, context) :
        #Prendo l'ultimo messaggio dalla coda
        while not (self.queue_metrics.empty()) :
            self.message = self.queue_metrics.get()

        #Se l'etl ha prodotto i dati calcolo le violazioni, altrimenti invio messaggio di errore
        if self.message :
            calculator_instance = MetricCalculator()
            result = calculator_instance.get_number_violation(request.listMetrics, str(self.message))
            return echo_pb2.resultValue(result=str(result))
        else : 
            return echo_pb2.resultValue(result='')

    def getNumberOfViolationsFuture(self, request, context) :
        #Prendo l'ultimo messaggio dalla coda
        while not (self.queue_predictions.empty()) :
            self.message_predictions = self.queue_predictions.get()

        #Se l'etl ha prodotto i dati calcolo le violazioni future, altrimenti invio messaggio di errore
        if self.message_predictions :
            calculator_instance = MetricCalculator()
            result = calculator_instance.get_number_future_violation(request.listMetrics, str(self.message_predictions))
            return echo_pb2.resultValue(result=str(result))
        else :
            return echo_pb2.resultValue(result='')
    
    
def serve(queue_metrics, queue_predictions):
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    #Passo le Queue all'Echo Service per far comunicare i processi
    echo_pb2_grpc.add_EchoServiceServicer_to_server(EchoService(queue_metrics, queue_predictions), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Echo Service started, listening on " + port)
    server.wait_for_termination()

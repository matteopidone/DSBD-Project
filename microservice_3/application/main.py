from flask import Flask, render_template
import grpc
import sys
sys.path.append('./gRPCUtils')
import echo_pb2
import echo_pb2_grpc
import ast

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/getAllMetrics")
def test():
    with grpc.insecure_channel('microservice_2:50051') as channel:
        stub = echo_pb2_grpc.EchoServiceStub(channel)
        query_result = stub.getAllMetrics(echo_pb2.emptyParam())
        if len(query_result.result) != 0 :
            query_result_list = list(ast.literal_eval(query_result.result))
            return render_template('metrics.html', results=query_result_list)
        else :
            return "<p>Nessuna Metrica al momento è disponibile</p>"

@app.route("/<id_metric>/metadata/")
def get_metadata_for_metrics(id_metric):
    with grpc.insecure_channel('microservice_2:50051') as channel:
        stub = echo_pb2_grpc.EchoServiceStub(channel)
        query_result = stub.getMetadataForMetrics(echo_pb2.idMetricParam(idMetric=id_metric))
        if len(query_result.result) != 0 :
            query_result_list = list(ast.literal_eval(query_result.result))
            return render_template('metrics_metadata.html', results=query_result_list)
        else :
            return "<p>Nessuna Metrica al momento è disponibile</p>"

@app.route("/<id_metric>/history/")
def get_history_for_metrics(id_metric):
    with grpc.insecure_channel('microservice_2:50051') as channel:
        stub = echo_pb2_grpc.EchoServiceStub(channel)
        query_result = stub.getHistoryForMetrics(echo_pb2.idMetricParam(idMetric=id_metric))
        if len(query_result.result) != 0 :
            query_result_list = list(ast.literal_eval(query_result.result))
            return render_template('metrics_history.html', results=query_result_list)
        else :
            return "<p>Nessuna Metrica al momento è disponibile</p>"

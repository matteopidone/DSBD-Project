from flask import Flask, render_template
import grpc
import sys
import os
sys.path.append('./gRPCUtils')
import echo_pb2
import echo_pb2_grpc
import ast

app = Flask(__name__)

@app.route("/")
def get_all_metrics():
    with grpc.insecure_channel(os.environ['DATA_STORAGE_GRPC_SERVER']) as channel:
        stub = echo_pb2_grpc.EchoServiceStub(channel)
        query_result = stub.getAllMetrics(echo_pb2.emptyParam())
        if len(query_result.result) != 0 :
            query_result_list = list(ast.literal_eval(query_result.result))
            return render_template('metrics.html', results=query_result_list)
        else :
            return "<p>Nessuna Metrica al momento è disponibile</p>"

@app.route("/<id_metric>/metadata")
def get_metadata_for_metrics(id_metric):
    with grpc.insecure_channel(os.environ['DATA_STORAGE_GRPC_SERVER']) as channel:
        stub = echo_pb2_grpc.EchoServiceStub(channel)
        query_result = stub.getMetadataForMetrics(echo_pb2.idMetricParam(idMetric=id_metric))
        if len(query_result.result) != 0 :
            query_result_list = list(ast.literal_eval(query_result.result))
            print(query_result_list)
            return render_template('metrics_metadata.html', results=query_result_list)
        else :
            return "<p>Nessuna Metrica al momento è disponibile</p>"

@app.route("/<id_metric>/history")
def get_history_for_metrics(id_metric):
    with grpc.insecure_channel(os.environ['DATA_STORAGE_GRPC_SERVER']) as channel:
        stub = echo_pb2_grpc.EchoServiceStub(channel)
        query_result = stub.getHistoryForMetrics(echo_pb2.idMetricParam(idMetric=id_metric))
        if len(query_result.result) != 0 :
            query_result_list = list(ast.literal_eval(query_result.result))
            return render_template('metrics_history.html', results=query_result_list)
        else :
            return "<p>Nessuna Metrica al momento è disponibile</p>"

@app.route("/<id_metric>/prediction")
def get_prediction_for_metrics(id_metric):
    with grpc.insecure_channel(os.environ['DATA_STORAGE_GRPC_SERVER']) as channel:
        stub = echo_pb2_grpc.EchoServiceStub(channel)
        query_result = stub.getPredictionForMetrics(echo_pb2.idMetricParam(idMetric=id_metric))
        if len(query_result.result) != 0 :
            query_result_list = list(ast.literal_eval(query_result.result))
            return render_template('metrics_prediction.html', results=query_result_list)
        else :
            return "<p>Nessuna Metrica al momento è disponibile</p>"

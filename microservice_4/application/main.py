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
def template_sla_manager():
    with grpc.insecure_channel(os.environ['DATA_STORAGE_GRPC_SERVER']) as channel:
        stub = echo_pb2_grpc.EchoServiceStub(channel)
        query_result_metrics = stub.getAllMetrics(echo_pb2.emptyParam())
        query_result_stats = stub.getAllStatistics(echo_pb2.emptyParam())
        if len(query_result_metrics.result) != 0 and len(query_result_stats.result) != 0 :
            list_metrics = list(ast.literal_eval(query_result_metrics.result))
            list_stats = list(ast.literal_eval(query_result_stats.result))
            return render_template('index.html', results=[list_metrics, list_stats])
        else :
            return "<p>Nessuna Metrica al momento è disponibile</p>"
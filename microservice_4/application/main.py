from flask import Flask, request, render_template
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

@app.route("/submitSLA", methods=['POST'])
def submit_sla():
    form_data = manage_data_form(request)
    with grpc.insecure_channel(os.environ['DATA_STORAGE_GRPC_SERVER']) as channel:
        stub = echo_pb2_grpc.EchoServiceStub(channel)
        result_past_violations = stub.getNumberOfViolationsPast(echo_pb2.listMetricsParam(form_data))
        result_future_violations = stub.getNumberOfViolationsFuture(echo_pb2.listMetricsParam(form_data))
        if len(result_past_violations.result) != 0 and len(result_future_violations.result) != 0 :
            past_violations = list(ast.literal_eval(result_past_violations.result))
            future_violations = list(ast.literal_eval(result_future_violations.result))
            return render_template('info_sla.html', results=[past_violations, future_violations])
        else :
            return "<p>Errore</p>"

""" Other Functions """

def manage_data_form(request):
    data_list = request.form.lists()
    metric_list = []
    
    for key, values in data_list:
        if key == 'metric_name':
            for value in values:
                metric_list.append({'metric_name': value, 'stats': []})
        else:
            if not values[0]:
                continue
            for metric in metric_list:
                if metric['metric_name'] != key.split("-")[0]:
                    continue
                metric['stats'].append({'name': key.split("-")[1], 'threshold': values[0]})
                break

    result = {"sla_metrics": metric_list}
    return result

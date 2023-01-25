from flask import Flask, render_template
import json
from connect_to_db import connect, close
import grpc
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
        result = stub.getAllMetrics(echo_pb2.getAllMetricsParams())
        print(list(ast.literal_eval(result.result)))
        return render_template('metrics.html', results=list(ast.literal_eval(result.result)))

@app.route("/<id_metric>/metadata/")
def get_metadata_for_metrics(id_metric):
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("Select nome, metadata FROM metriche WHERE id = %s LIMIT 1", (id_metric,))
        query_result = cursor.fetchone()
        if query_result :
            return  render_template('metrics_metadata.html', results=query_result)
        else :
            return "<p>Nessuna Metrica al momento è disponibile</p>"
    except Error as e:
        print("Error while execute the query", e)
    finally:
        cursor.close()
        close(database)

@app.route("/<id_metric>/history/")
def get_metadata_for_metrics_2(id_metric):
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("SELECT metriche.nome, statistiche.nome, statistiche_metriche.1h, statistiche_metriche.3h, statistiche_metriche.12h FROM metriche JOIN statistiche_metriche ON metriche.id=statistiche_metriche.id_metrica JOIN statistiche on statistiche.id=statistiche_metriche.id_statistica WHERE metriche.id= %s", (id_metric,))
        query_result = cursor.fetchall()
        if query_result :
            return  render_template('metrics_history.html', results=query_result)
        else :
            return "<p>Nessuna Metrica al momento è disponibile</p>"
    except Error as e:
        print("Error while execute the query", e)
    finally:
        cursor.close()
        close(database)

@app.route("/test/json")
def test_json():
    return json.dumps(data)
    #return json.dumps({"key0":"value0", "key_key":{"key1":"value1", "key2":"value2"}})
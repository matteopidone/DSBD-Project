from flask import Flask, render_template
import json
from connect_to_db import connect, close

app = Flask(__name__)

def execute(query):
    database = connect()
    cursor = database.cursor()
    data = False
    try:
        cursor.execute(query)
        data = cursor
    except Error as e:
        print("Error while execute the query", e)
    print(data)
    return data


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/getAllMetrics")
def test():
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("SELECT * FROM statistiche")
        query_result = cursor.fetchall()
        if query_result :
            return render_template('metrics.html', results=query_result)
        else :
            return "<p>Nessuna Metrica al momento è disponibile</p>"
    except Error as e:
        print("Error while execute the query", e)
    finally:
        cursor.close()
        close(database)

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

@app.route("/test/json")
def test_json():
    return json.dumps(data)
    #return json.dumps({"key0":"value0", "key_key":{"key1":"value1", "key2":"value2"}})
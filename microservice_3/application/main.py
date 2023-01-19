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
    cursor.execute("SELECT * FROM statistiche")
    '''
    if(data == False):
        return "<p>Errore, riprovare più tardi</p>"
    '''  
    query_result = cursor.fetchall()
    cursor.close()
    close(database)
    return render_template('metrics.html', results=query_result)

@app.route("/<id_metric>/metadata/")
def get_metadata_for_metrics(id_metric):
    database = connect()
    cursor = database.cursor()
    cursor.execute("Select nome, metadata FROM metriche WHERE id = %s LIMIT 1", (id_metric,))
    name, metadata = cursor.fetchone()
    response = "<h1 style='text-align: center'>Lista di Metadati per " + str(name) +"</h1><table><tr><th>Metadati</th></tr>"
    response = response + "<tr><td>" + str(metadata) + "</td></tr></table>"
    cursor.close()
    close(database)
    return response

@app.route("/test/json")
def test_json():
    return json.dumps(data)
    #return json.dumps({"key0":"value0", "key_key":{"key1":"value1", "key2":"value2"}})
from flask import Flask
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
    response = "<h1 style='text-align: center'>Lista di Metriche</h1><table><tr><th>ID Metrica</th><th>Nome Metrica</th></tr>"
    for (id, nome) in cursor:
        response = response + "<tr><td>" + str(id) + "</td>" + "<td>" + nome + "</td><tr>"
    response = response + "</table>"
    cursor.close()
    close(database)
    return response

@app.route("/test/json")
def test_json():
    return json.dumps(data)
    #return json.dumps({"key0":"value0", "key_key":{"key1":"value1", "key2":"value2"}})
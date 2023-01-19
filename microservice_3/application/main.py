from flask import Flask
import json
from connect_to_db import connect

app = Flask(__name__)

database = connect()
cursor = database.cursor()
data = cursor.execute("SHOW TABLES")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    return data

@app.route("/test/json")
def test_json():
    return json.dumps(data)
    #return json.dumps({"key0":"value0", "key_key":{"key1":"value1", "key2":"value2"}})
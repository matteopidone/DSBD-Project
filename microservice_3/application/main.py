from flask import Flask
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    return "<h1>Test !!</h1>"

@app.route("/test/json")
def test_json():
    return json.dumps({"key0":"value0", "key_key":{"key1":"value1", "key2":"value2"}})
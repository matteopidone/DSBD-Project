from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def template_sla_manager():
    return render_template('file.html', results=['cpu', 'memory', 'network'])

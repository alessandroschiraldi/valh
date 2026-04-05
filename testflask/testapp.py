from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route("/suckers")
def hello_world():
    return "<p>Hello, fuckers!!</p>"
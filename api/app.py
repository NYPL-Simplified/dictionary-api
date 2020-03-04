from flask import Flask
from nose.tools import set_trace

app = Flask(__name__)
url = app.config.from_object('config')
  
import api.routes

@app.route("/")
def main():
    return "main page for dictionary api"


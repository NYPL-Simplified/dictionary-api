from flask import Flask

app = Flask(__name__)

from . import routes

def run():
  debug = True
  app.run(debug=debug)

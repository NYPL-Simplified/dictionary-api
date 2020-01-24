from flask import Flask

app = Flask(__name__)
url = app.config.from_object('config')

from . import routes

def run():
  debug = True
  app.run(debug=debug)

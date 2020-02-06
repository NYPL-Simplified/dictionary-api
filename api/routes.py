from flask import (
  request,
  jsonify,
  Response,
)
from flask_babel import lazy_gettext as _
from nose.tools import set_trace
from api.app import app
from api.controller.manager import (
  setup_controllers,
  Manager,
)
from core.app_server import (
  feed_response
)

@app.before_first_request
def setup():
  app.manager = Manager()
  setup_controllers(app.manager)

@app.route("/<word>/definition/<language>/", methods=["GET"])
def definition(word, language):
  feed = app.manager.dictionary_controller.definition(word, language)
  
  return feed_response(feed)

@app.route("/<word>/translation/<language_from>/", methods=["GET"])
def translation(word, language_from):
  # TODO
  return Response(_("Success"), 200)

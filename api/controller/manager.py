from nose.tools import set_trace
import flask
import logging
from ..elastic_search import ExternalSearchIndex
from .dictionary import Dictionary
from api.app import app

def setup_controllers(manager):
  url = app.config["ELASTIC_SEARCH_URL"]
  manager.dictionary_controller = Dictionary(ExternalSearchIndex, url)

class Manager(object):
  def __init__(self):
    self.log = logging.getLogger("Dictionary Manager")

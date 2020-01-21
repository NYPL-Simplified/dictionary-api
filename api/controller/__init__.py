from pdb import set_trace
import flask
import logging
from ..elastic_search import ExternalSearchIndex
from .dictionary import Dictionary

def setup_controllers(manager):
  manager.dictionary_controller = Dictionary(ExternalSearchIndex)

class Manager(object):
  def __init__(self):
    self.log = logging.getLogger("Dictionary Manager")

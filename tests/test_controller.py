from nose.tools import (
  eq_,
  set_trace,
  assert_is_instance
)
from api.app import app
from api.controller.manager import (
  Manager,
  setup_controllers,
)
from api.controller.dictionary import (
  Dictionary,
  MockDictionary,
)
from api.elastic_search import MockExternalSearchIndex

class TestController(object):
  def setup(self):
    es_url = app.config["ELASTIC_SEARCH_URL"]
    app.manager = Manager()
    app.manager.dictionary_controller = Dictionary(MockExternalSearchIndex, es_url)
    self.app = app

    self.example_results = []
    external_search = app.manager.dictionary_controller.external_search
    # Insert documents into the test Elastic Search instance
    for doc in external_search.elastic_search_results():
      external_search.insert(doc)

class TestManager(object):
  def test_init(self):
    manager = Manager()
    setup_controllers(manager)

    assert_is_instance(
      manager.dictionary_controller,
      Dictionary
    )


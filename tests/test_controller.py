from nose.tools import (
  assert_raises,
  eq_,
  set_trace,
  assert_is_instance
)
from api.app import app
from api.controller import (
  Manager,
  setup_controllers,
)
from api.controller.dictionary import (
  Dictionary,
  MockDictionary,
)
from api.elastic_search import ExternalSearchIndex

class TestController(object):
  def setup(self):
    self.app = app
    self.manager = Manager()
    self.manager.dictionary_controller = MockDictionary(ExternalSearchIndex)

class TestManager(object):
  def test_init(self):
    manager = Manager()
    setup_controllers(manager)

    assert_is_instance(
      manager.dictionary_controller,
      Dictionary
    )


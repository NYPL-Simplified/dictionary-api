from nose.tools import (
  assert_raises,
  eq_,
  set_trace,
  assert_is_instance
)
from api.controller.dictionary import (
  MockDictionary,
)
from api.elastic_search import ExternalSearchIndex

class TestDictionary(object):
  def setup(self):
    self.dictionary = MockDictionary(ExternalSearchIndex)

  def test_combine_definitions(self):
    pass

  def test_definition(self):
    eq_(self.dictionary.definition('test'), dict(
      word="test",
      definitions=[
        dict(glosses=["first definition"]),
        dict(glosses=["second definition"], tags=["transitive"])
      ]
    ))

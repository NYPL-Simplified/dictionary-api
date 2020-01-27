from nose.tools import (
  eq_,
  set_trace,
)
from api.controller.dictionary import (
  Dictionary,
)
from api.elastic_search import MockExternalSearchIndex
from api.app import app

class TestDictionary(object):
  def setup(self):
    es_url = app.config["ELASTIC_SEARCH_URL"]
    self.dictionary = Dictionary(MockExternalSearchIndex, es_url)
    external_search = self.dictionary.external_search
    # Insert documents into the test Elastic Search instance
    for doc in external_search.elastic_search_results():
      external_search.insert(doc)

  def test_definition(self):
    # Get the example search result for word 'dictionary'.
    (ignore, ignore2, ignore3, doc) = self.dictionary.external_search.elastic_search_results()
    definitions = doc["senses"]
    word = 'dictionary'

    eq_(
      self.dictionary.definition(word),
      dict(word=word, definitions=definitions)
    )

  def test_combine_definitions(self):
    # Mock set of Elastic Search results for word 'dictionary'.
    (ignore, ignore2, doc, doc2) = self.dictionary.external_search.elastic_search_results()
    example_combined = doc["senses"] + doc2["senses"]

    # We just want the actual definitions for a word and not the
    # other values in a search result hit.
    definitions = self.dictionary.combine_definitions([doc, doc2])

    eq_(definitions, example_combined)


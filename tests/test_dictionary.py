from nose.tools import (
  eq_,
  set_trace,
)
from api.controller.dictionary import (
  Dictionary,
)
from api.elastic_search import MockExternalSearchIndex
from api.app import app
from api.opds import DictionaryFeed

class TestDictionary(object):
  def setup(self):
    es_url = app.config["ELASTIC_SEARCH_URL"]
    self.dictionary = Dictionary(MockExternalSearchIndex, es_url)
    external_search = self.dictionary.external_search
    # Insert documents into the test Elastic Search instance
    for doc in external_search.elastic_search_results():
      external_search.insert(doc)

  def test_definition(self):
    url = "/dictionary/definition/English/"
    word = 'dictionary'

    with app.test_request_context(url) as c:
      # Get test example search results for word 'dictionary'.
      (ignore, ignore2, doc1, doc2) = self.dictionary.external_search.elastic_search_results()
      # Manually compile the definitions and build the expected feed.
      definitions = self.dictionary.combine_definitions([doc2])
      dictionaryFeed = DictionaryFeed(word, url, "English", definitions)
      expected_feed = dictionaryFeed.get_feed()

      # The result feed after searching for the word in Elastic Search
      # and building it.
      definition_json = self.dictionary.definition(word)

      # Don't worry about testing the time...
      del definition_json["metadata"]["modified"]
      del expected_feed["metadata"]["modified"]

      eq_(definition_json["metadata"], expected_feed["metadata"])
      eq_(definition_json['links'], expected_feed["links"])
      eq_(definition_json["definitions"], expected_feed["definitions"])

  def test_combine_definitions(self):
    # Mock set of Elastic Search results for word 'dictionary'.
    (ignore, ignore2, doc, doc2) = self.dictionary.external_search.elastic_search_results()
    example_combined = doc["senses"] + doc2["senses"]

    # We just want the actual definitions for a word and not the
    # other values in a search result hit.
    definitions = self.dictionary.combine_definitions([doc, doc2])

    eq_(definitions, example_combined)


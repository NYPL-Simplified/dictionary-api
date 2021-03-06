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
    url = "/dictionary/definition/en/"
    word = "dictionary"

    # We expect to get results from Elasticsearch when the
    # word is 'dictionary' and the language is 'en'.
    with app.test_request_context(url) as c:
      # Get the example search result for word 'dictionary'.
      (ignore, ignore2, ignore3, doc) = self.dictionary.external_search.elastic_search_results()
      definitions = doc["senses"]
      for definition in definitions:
        # Testing with only one definition per "glosses" so end result is
        # only a string.
        definition["metadata"] = definition["glosses"][0]
        definition["pos"] = doc["pos"]
        del definition["glosses"]

      definition_json = self.dictionary.definition(word)
      # Don't worry about testing the time...
      del definition_json["metadata"]["modified"]

      eq_(
        definition_json["metadata"],
        {
          "title": "Definitions for dictionary",
          "@type": "http://schema.org/DefinedTerm",
          "language": "en",
          "name": "dictionary"
        }
      )
      eq_(definition_json["links"],
        [{"rel": "self", "href": url, "type": "application/opds+json"}]
      )
      eq_(definition_json["definitions"],
        definitions
      )

    url = "/dictionary/definition/es/"
    # We do not expect to get results from Elasticsearch when the
    # word is 'dictionary' and the language is 'es'.
    with app.test_request_context(url) as c:
      definition_json = self.dictionary.definition(word, 'es')
      # Don't worry about testing the time...
      del definition_json["metadata"]["modified"]

      eq_(
        definition_json["metadata"],
        {
          "title": "Definitions for dictionary",
          "@type": "http://schema.org/DefinedTerm",
          "language": "es",
          "name": "dictionary"
        }
      )
      eq_(definition_json["links"],
        [{"rel": "self", "href": url, "type": "application/opds+json"}]
      )
      # Should not return any results since there are no documents with
      # 'es' as the language for the definition of the word
      eq_(definition_json["definitions"], [])

  def test_combine_definitions(self):
    # Mock set of Elastic Search results for word "dictionary".
    (ignore, ignore2, doc, doc2) = self.dictionary.external_search.elastic_search_results()
    example_combined = doc["senses"] + doc2["senses"]

    # We just want the actual definitions for a word and not the
    # other values in a search result hit.
    definitions = self.dictionary.combine_definitions([doc, doc2])

    eq_(definitions, example_combined)


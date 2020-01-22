import logging
from elasticsearch import Elasticsearch
from nose.tools import (
  assert_raises,
  eq_,
  set_trace,
  assert_is_instance
)
from api.elastic_search import (
  ExternalSearchIndex,
  MockExternalSearchIndex,
)

class TestExternalSearchIndex():
  def setup(self):
    self.es = MockExternalSearchIndex()

  def test_insert_doc(self):
    doc = {"id": 1, "word": "cat", "definitions": ["feline", "domestic animal"]}
    doc2 = {"id": 2, "word": "dog", "definitions": ["bark"]}
    self.es.insert_doc(doc)
    self.es.insert_doc(doc2)

    eq_(self.es.docs, {
      (self.es.DEFAULT_INDEX, self.es.DEFAULT_TYPE, doc["id"]): doc,
      (self.es.DEFAULT_INDEX, self.es.DEFAULT_TYPE, doc2["id"]): doc2,
    })

  def test_search_doc(self):
    doc = {"id": 1, "word": "cat", "definitions": ["feline", "domestic animal"]}
    doc2 = {"id": 2, "word": "dog", "definitions": ["bark"]}
    self.es.insert_doc(doc)
    self.es.insert_doc(doc2)

    eq_(self.es.search_doc("cat"), doc)

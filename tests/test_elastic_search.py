import logging
from elasticsearch import Elasticsearch
from nose.tools import (
  eq_,
  set_trace,
)
from api.elastic_search import (
  ExternalSearchIndex,
  MockExternalSearchIndex,
)

class TestExternalSearchIndex():
  def setup(self):
    self.es = MockExternalSearchIndex()

  def test_insert(self):
    # Example set of Elastic Search result documents
    (doc, doc2, ignore, ignore2) = self.es.elastic_search_results()
    self.es.insert(doc)
    self.es.insert(doc2)

    eq_(self.es.docs, {
      (self.es.DEFAULT_INDEX, self.es.DEFAULT_TYPE, doc['word']): doc,
      (self.es.DEFAULT_INDEX, self.es.DEFAULT_TYPE, doc2['word']): doc2,
    })

  def test_search_for(self):
    (doc, doc2, ignore, ignore2) = self.es.elastic_search_results()
    self.es.insert(doc)
    self.es.insert(doc2)

    eq_(self.es.search_for("cat"), [doc])
    eq_(self.es.search_for("dog"), [doc2])
    eq_(self.es.search_for("bird"), [{}])

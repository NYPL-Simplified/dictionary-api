import logging
from elasticsearch import Elasticsearch
from nose.tools import set_trace

class ExternalSearchIndex():
  DEFAULT_INDEX = 'dictionary'
  DEFAULT_TYPE = 'words'
  __client = None

  def __init__(self):
    self.log = logging.getLogger("External search index")

    if not ExternalSearchIndex.__client:
      self.log.info(
        "Connecting to index %s in Elasticsearch cluster at %s",
        self.DEFAULT_INDEX, 'localhost:9200'
      )
      ExternalSearchIndex.__client =  Elasticsearch([{'host': 'localhost', 'port': 9200}])

    self.indices = self.__client.indices
    self.index = self.__client.index
    self.delete = self.__client.delete
    self.exists = self.__client.exists
    self.search = self.__client.search
    self.work_alias = "dictionary-words"
  
  def insert_doc(self, doc):
    self.index(self.DEFAULT_INDEX, self.DEFAULT_TYPE, body=doc)

  def search_doc(self, word, language="English"):
    results = self.search(
      index=self.DEFAULT_INDEX, doc_type=self.DEFAULT_TYPE,
      body={'query': {'match': { 'word': word}}}
    )

    return self.get_hits(results)

  def get_hits(self, results):
    data = [hit['_source'] for hit in results['hits']['hits']]

    return data

class MockExternalSearchIndex(ExternalSearchIndex):
  def __init__(self):
    self.docs = {}
    self.log = logging.getLogger("Mock External Search Index")
  
  def _key(self, index, doc_type, word):
    return (index, doc_type, word)
  
  def index(self, index, doc_type, body):
    self.docs[self._key(index, doc_type, body['word'])] = body
  
  def search(self, index, doc_type, body):
    word = body['query']['match']['word']
    key = (self.DEFAULT_INDEX, self.DEFAULT_TYPE, word)
    
    return self.docs.get(key, {})
  
  def get_hits(self, results):
    return results


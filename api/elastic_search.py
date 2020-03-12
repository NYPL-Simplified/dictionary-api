import logging
from elasticsearch import Elasticsearch
from nose.tools import set_trace
from .languages import LanguageCodes, LanguageNames

class ExternalSearchIndex():
  DEFAULT_INDEX = 'dictionary'
  DEFAULT_TYPE = 'words'
  __client = None

  def __init__(self, url):
    self.log = logging.getLogger("External search index")

    if not ExternalSearchIndex.__client:
      self.log.info(
        "Connecting to index %s in Elasticsearch cluster at %s",
        self.DEFAULT_INDEX, url
      )
      ExternalSearchIndex.__client = Elasticsearch([url])

    self.indices = self.__client.indices
    self.index = self.__client.index
    self.delete = self.__client.delete
    self.exists = self.__client.exists
    self.search = self.__client.search
    self.work_alias = "dictionary-words"
  
  def insert(self, doc):
    self.index(self.DEFAULT_INDEX, self.DEFAULT_TYPE, body=doc)

  def search_for(self, word, language="en"):
    results = self.search(
      index=self.DEFAULT_INDEX, doc_type=self.DEFAULT_TYPE,
      body={'query': {'bool': { 'must': [
        { 'match': { 'word': word }},
        { 'match': { 'lang': language }},
      ]}}}
    )

    return self.get_hits(results)

  def get_hits(self, results):
    data = [hit['_source'] for hit in results['hits']['hits']]

    return data

class MockExternalSearchIndex(ExternalSearchIndex):
  def __init__(self, url):
    self.url = url
    self.docs = {}
    self.log = logging.getLogger("Mock External Search Index")
  
  def _key(self, index, doc_type, word):
    return (index, doc_type, word)
  
  def index(self, index, doc_type, body):
    self.docs[self._key(index, doc_type, body['word'])] = body
  
  def search(self, index, doc_type, body):
    must = body['query']['bool']['must']
    [word, lang] = [x['match'] for x in must]
    key = (self.DEFAULT_INDEX, self.DEFAULT_TYPE, word['word'])
    
    return [self.docs.get(key, {})]

  def get_hits(self, results):
    return results

  def elastic_search_results(self):
    doc = {"word": "cat", "lang": "en", "senses": [{"glosses": ["feline"]}, {"glosses": ["domestic animal"]}]}
    doc2 = {"word": "dog", "lang": "en", "senses": [{"glosses": ["bark"]}]}
    doc3 = {"lang": "en", "senses": [{"glosses": ["A reference work with a list of words from one or more languages, normally ordered alphabetically, explaining each word's meaning, and sometimes containing information on its etymology, pronunciation, usage, translations, and other data."]}, {'glosses': ['Any work that has a list of material organized alphabetically; e.g., biographical dictionary, encyclopedic dictionary.'], 'tags': ['by extension']}, {'glosses': ['An associative array, a data structure where each value is referenced by a particular key, analogous to words and definitions in a physical dictionary.'], 'tags': ['computing']}], 'word': 'dictionary', 'pos': 'noun'}
    doc4 = {"lang": "en", "senses": [{"glosses": ["To look up in a dictionary."], "tags": ["transitive"]}, {"glosses": ["To add to a dictionary."], "tags": ["transitive"]}, {"glosses": ["To compile a dictionary."], "tags": ["rare", "intransitive"]}, {"glosses": ["To appear in a dictionary."], "tags": ["intransitive"]}], "word": "dictionary", "pos": "verb"}
    return (doc, doc2, doc3, doc4)

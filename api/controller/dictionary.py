from nose.tools import set_trace
from api.opds import DictionaryFeed
from flask import url_for

class Dictionary(object):
  def __init__(self, external_search, es_url):
    self.external_search = external_search(es_url)

  def _search(self, word, language):
    '''Searches ES for definitions based on word and language.
    :param word: word to define
    :param language: the language of the word
    :return: a list of definition objects with 'glosses' and 'tags' properties
    '''
    es_results = self.external_search.search_for(word, language)
    definitions = self.combine_definitions(es_results)
    return definitions

  def definition(self, word, language="English"):
    definitions = self._search(word, language)
    url = url_for(
      "definition",
      word=word,
      language=language
    )
    feed = DictionaryFeed(word, url, language, definitions)

    return feed.get_feed()
  
  def combine_definitions(self, words):
    '''Each word entry contains a list of "senses" and a "pos" (part-of-speech).
    Here we combine all "glosses" in every entry's "senses" list, but also add
    the part-of-speech.
    '''
    definition_objects = [(word['senses'], word.get('pos', None)) for word in words]
    definitions = []

    for sense, pos in definition_objects:
      if pos:
        for s in sense:
          s['pos'] = pos
      definitions += sense

    return definitions

  def translation(self, word, language_from):
    return NotImplemented

class MockDictionary(Dictionary):
  def definition(self, word, language="English"):
    # Mock a set of elastic search results for word 'dictionary'.
    results = self.external_search.elastic_search_results()
    definitions = self.combine_definitions(results)

    return dict(
      word=word,
      definitions=definitions
    )

from nose.tools import set_trace

class Dictionary(object):
  def __init__(self, external_search):
    self.external_search = external_search()

  def definition(self, word, language="English"):
    results = self.external_search.search_for(word, language)
    
    definitions = self.combine_definitions(results)

    return dict(
      word=word,
      definitions=definitions,
    )
  
  def combine_definitions(self, words):
    senses = [word['senses'] for word in words]
    definitions = []
    for sense in senses:
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

from nose.tools import set_trace

class Dictionary(object):
  def __init__(self, external_search):
    self.external_search = external_search()

  def definition(self, word, language="English"):
    results = self.external_search.search_doc(word, language)
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
    return dict(
      word=word,
      definitions=[
        dict(glosses=["first definition"]),
        dict(glosses=["second definition"], tags=["transitive"])
      ]
    )

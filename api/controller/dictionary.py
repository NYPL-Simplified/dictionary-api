from pdb import set_trace

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
      defs = [s['glosses'][0] for s in sense]
      definitions += defs

    return definitions

  def translation(self, word, language_from):
    return NotImplemented

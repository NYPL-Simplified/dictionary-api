from nose.tools import set_trace
from core.util.opds_writer import (
  OPDSFeed
)
from flask import url_for

class DictionaryFeed(OPDSFeed):

  def __init__(self, word, language):
    self.word = word
    self.language = language
    # todo: use url_for for this url
    self.feed = OPDSFeed(
      title=self.word,
      url=url_for(
        "definition",
        word=word,
        language=language
      )
    )

  def get_feed(self, definitions):
    self.add_definitions(definitions)
    return self.feed.feed
  
  def add_definitions(self, definitions):
    '''Adds entries for each definition.

    :param definitions: a list of definition objects with 'glosses' and
      'tags' properties
    '''
    entries = [self.add_entry(definition) for definition in definitions]

  def add_entry(self, definition):
    '''Adds entries for each definition.

    :param definition: an objects with 'glosses' and 'tags' properties
    '''
    elements = []

    for d in definition.get("glosses", []):
      definition_element = OPDSFeed.makeelement("definition")
      definition_element.text = d
      elements.append(definition_element)
    for t in definition.get("tags", []):
      tag_element = OPDSFeed.makeelement("tag")
      tag_element.text = t
      elements.append(tag_element)

    entry = OPDSFeed.entry(*elements)

    self.feed.feed.append(entry)

    return entry

from nose.tools import set_trace
from opds.opds_writer import OPDSFeed

class DictionaryFeed(OPDSFeed):
  SCHEMA_DEFINED_TERM_SET = "http://schema.org/DefinedTermSet"
  SCHEMA_DEFINED_TERM = "http://schema.org/DefinedTerm"
  TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ%z'

  def __init__(self, word, url, language, definitions):
    super().__init__(word, url)

    self.language = language
    self.feed["definitions"] = []

    self.add_metadata()
    self.add_definitions(definitions)

  def add_metadata(self):
    super().add_metadata()
    self.metadata["title"] = "Definitions for %s" % self.title
    self.metadata["@type"] = self.SCHEMA_DEFINED_TERM_SET
    self.metadata["language"] = self.language
    self.metadata["name"] = self.title

  def get_feed(self):
    return self.feed
  
  def __str__(self):
    set_trace()
    return str(self.feed)

  def add_definitions(self, definitions):
    '''Adds entries for each definition.
    :param definitions: a list of definition objects with 'glosses', 'pos',
      and 'tags' properties coming from Wiktionary.
    '''
    entries = [self.add_entry(definition) for definition in definitions]

  def add_entry(self, definition):
    '''Adds entries for each definition.
    :param definition: an objects with 'glosses' and 'tags' properties
    '''

    definition_element = None
    definitions = []
    for d in definition.get("glosses", []):
      subjects = [dict(name=s,code=s,schema="tbd") for s in definition.get("tags", [])]
      metadata = {
        "pos": definition.get("pos", None),
        "subject": subjects,
        "@type": self.SCHEMA_DEFINED_TERM,
        "description": d,
        "name": self.title,
        "language": self.language,
      }
      definition_element = dict(metadata=metadata)
      definitions.append(definition_element)

    self.feed["definitions"] += definitions
    return definition_element

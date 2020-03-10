from nose.tools import set_trace
from api.opds.opds_writer import OPDSFeed
from functools import reduce
import json
from .languages import LanguageCodes

class DictionaryFeed(OPDSFeed):
  SCHEMA_DEFINED_TERM = "http://schema.org/DefinedTerm"
  TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ%z'

  def __init__(self, word, url, language, raw_definitions):
    super().__init__(word, url)

    self.language = self.update_language_code(language)
    self.add_metadata()
    self.definitions = self.update_definitions(raw_definitions)

  def add_metadata(self):
    super().add_metadata()
    self.metadata["title"] = "Definitions for %s" % self.title
    self.metadata["@type"] = self.SCHEMA_DEFINED_TERM
    self.metadata["language"] = self.language
    self.metadata["name"] = self.title
  
  def update_language_code(self, language):
    alpha_3 = LanguageCodes.string_to_alpha_3(language)
    alpha_2 = LanguageCodes.three_to_two[alpha_3]

    return alpha_2

  def get_feed(self):
    ns = self.builder.build_classes()
    definition_builder = ns.Definition
    definitions = definition_builder(
      title=self.title,
      metadata=self.metadata,
      definitions=self.definitions,
      links=self.links
    )

    return json.loads(definitions.serialize())

  def update_definitions(self, raw_definitions):
    '''Adds entries for each definition after normalizing the data.
    :param raw_definitions: a list of definition objects with 'glosses', 'pos',
      and 'tags' properties coming from Wiktionary.
    '''
    if not len(raw_definitions):
      return []

    defs = [self.update_entry(definition) for definition in raw_definitions]
    definitions = reduce(lambda x, y: x + y, defs)

    return definitions

  def update_entry(self, definition):
    '''Updates each definition by converting the "glosses" key property
    into a "metadata" key property.
    :param definition: an objects with 'glosses' and 'tags' properties
    '''

    definition_element = None
    definitions = []
    for d in definition.get("glosses", []):
      definition_element = dict(
        metadata=d,
        tags=definition.get("tags", []),
        pos=definition.get("pos", None)
      )
      definitions += [definition_element]

    return definitions

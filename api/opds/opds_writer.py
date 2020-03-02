import datetime
import logging

from nose.tools import set_trace
import json
import os
import python_jsonschema_objects as pjs

class MyClassBuilder(pjs.classbuilder.ClassBuilder):
  def _construct(self, uri, clsdata, *args, **kwargs):
    # Remove unsupported features from the schema before trying to
    # process it.
    clsdata.pop('anyOf', None)
    return super()._construct(uri, clsdata, *args, **kwargs)

pjs.classbuilder.ClassBuilder = MyClassBuilder

class OPDSFeed(object):
    FEED_TYPE = "application/opds+json"
    SCHEMA_BOOK = "http://schema.org/Book"
    # Latest supported version according to python_jsonschema_objects's code.
    JSON_SCHEMA = "http://json-schema.org/draft-04/schema#"

    def __init__(self, title, url, schema_file):
        self.title = title
        self.url = url
        self.links = [
            dict(rel="self", href=url, type=self.FEED_TYPE)
        ]
        self.schema = json.load(open(os.path.abspath(schema_file)))
        self.builder = pjs.ObjectBuilder(self.schema)

    def add_metadata(self):
        now = datetime.datetime.utcnow()
        modified = now.strftime(self.TIME_FORMAT)
        self.metadata = {
            "title": self.title,
            "@type": self.SCHEMA_BOOK,
            "modified": modified
        }

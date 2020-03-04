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
    JSON_SCHEMA_FILE = "api/schema/simple.json"

    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.links = [
            dict(rel="self", href=url, type=self.FEED_TYPE)
        ]
        self.schema = json.load(open(os.path.abspath(self.JSON_SCHEMA_FILE)))
        self.builder = pjs.ObjectBuilder(self.schema)

    def add_metadata(self):
        now = datetime.datetime.utcnow()
        modified = now.strftime(self.TIME_FORMAT)
        self.metadata = {
            "title": self.title,
            "@type": self.SCHEMA_BOOK,
            "modified": modified
        }


import datetime
import logging

from nose.tools import set_trace

class OPDSFeed(object):
    FEED_TYPE = "application/opds+json"
    SCHEMA_BOOK = "http://schema.org/Book"

    def __init__(self, title, url):
        self.title = title
        self.feed = {}
        self.feed["links"] = [
            dict(rel="self", href=url, type=self.FEED_TYPE)
        ]

    def add_metadata(self):
        now = datetime.datetime.utcnow()
        modified = now.strftime(self.TIME_FORMAT)
        self.metadata = {
            "title": self.title,
            "@type": self.SCHEMA_BOOK,
            "modified": modified
        }
        self.feed["metadata"] = self.metadata


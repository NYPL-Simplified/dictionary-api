import json
from nose.tools import set_trace
import wiktextract
from datetime import datetime

from .elastic_search import ExternalSearchIndex

class WiktionaryExtract(object):
    def __init__(self, url=None):
        self.external_search = ExternalSearchIndex()
        self.url = url

    def run(self):
        ctx = wiktextract.parse_wiktionary(
            self.url,
            self.wiktextract_word_cb,
            capture_cb=None,
            languages=["English"],
            translations=False,
            pronunciations=False,
            redirects=False
        )

        return ctx

    def wiktextract_word_cb(self, word, *args, **kwargs):
        self.clean_word(word)
        self.external_search.insert_doc(word)

    def clean_word(self, word):
        if 'translations' in word:
            word['translations'] = [
                t for t in x['translations'] if t['lang'] in ('ar', 'es')
            ]

        for ignore in [
            'categories', 'heads', 'conjugation', 'hyphenation', 'pinyin', 'synonyms',
            'antonyms', 'hypernyms', 'holonyms', 'meronyms', 'derived', 'related',
            'pronunciations', 'translations'
        ]:
            if ignore in word:
                del word[ignore]

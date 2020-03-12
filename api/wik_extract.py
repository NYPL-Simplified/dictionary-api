import json
from nose.tools import set_trace
import wiktextract
from datetime import datetime
from .app import app
from .languages import LanguageCodes

class WiktionaryExtract(object):
    def __init__(self, url, external_search, wiktextract=wiktextract):
        es_url = app.config["ELASTIC_SEARCH_URL"]
        self.external_search = external_search(es_url)
        self.wiktextract = wiktextract
        self.url = url

    def run(self):
        if self.url is None:
            raise ValueError("No 'url' value is set")

        ctx = self.wiktextract.parse_wiktionary(
            self.url,
            self.wiktextract_word_cb,
            capture_cb=None,
            # Should be updated to get more languages
            languages=["English"],
            translations=False,
            pronunciations=False,
            redirects=False
        )

        return ctx

    def wiktextract_word_cb(self, word, *args, **kwargs):
        self.clean_word(word)
        self.external_search.insert(word)

    def update_language(self, language):
        '''Update the language string into the equivalent language code. This
        is language value that will go into the Elasticsearch document.
        '''
        if len(language) != 2 or len(language) != 3:
            alpha_3 = LanguageCodes.string_to_alpha_3(language)
            alpha_2 = LanguageCodes.three_to_two[alpha_3]
            return alpha_2
        return language

    def clean_word(self, word):
        # Remove all but Arabic and Spanish translations
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

        word['lang'] = self.update_language(word['lang'])

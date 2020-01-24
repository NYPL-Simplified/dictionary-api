from nose.tools import (
  eq_,
  set_trace,
  assert_raises,
)
from api.wik_extract import WiktionaryExtract
from api.elastic_search import (
  ExternalSearchIndex,
  MockExternalSearchIndex,
)

class MockWiktExtract(object):
  def parse_wiktionary(self, url, cb, *args, **kwargs):
    self.url = url
    self.cb = cb
    self.args = args
    self.kwargs = kwargs

class TestWiktionaryExtract(object):
  def test_run_no_url(self):
    wiktionaryExtract = WiktionaryExtract(None, ExternalSearchIndex)

    assert_raises(ValueError, wiktionaryExtract.run)

  def test_run(self):
    # Test that the wiktextract package was called when the run()
    # method is called with the appropriate values.
    mockWiktExtract = MockWiktExtract()
    wiktionaryExtract = WiktionaryExtract("some-url", ExternalSearchIndex, mockWiktExtract)

    wiktionaryExtract.run()

    # The url path to the wiktionary dataset is what we care about the most.
    eq_(mockWiktExtract.url, "some-url")
    # The callback function passed to the wiktextract package.
    eq_(mockWiktExtract.cb, wiktionaryExtract.wiktextract_word_cb)
    # Default values passed to the wiktextract package.
    eq_(mockWiktExtract.kwargs, {
      'capture_cb': None,
      'languages': ['English'],
      'translations': False,
      'pronunciations': False,
      'redirects': False
    })

  def test_wiktexttract_word_cb(self):
    mockWiktExtract = MockWiktExtract()
    wiktionaryExtract = WiktionaryExtract(
      "some-url",
      MockExternalSearchIndex,
      mockWiktExtract
    )

    mockExternalSearchIndex = wiktionaryExtract.external_search
    (doc, doc2, ignore2, ignore3) = mockExternalSearchIndex.elastic_search_results()

    wiktionaryExtract.wiktextract_word_cb(doc)
    all_docs = mockExternalSearchIndex.docs

    eq_(all_docs, {
      ('dictionary', 'words', 'cat'): doc,
    })

    wiktionaryExtract.wiktextract_word_cb(doc2)
    all_docs = mockExternalSearchIndex.docs

    eq_(all_docs, {
      ('dictionary', 'words', 'cat'): doc,
      ('dictionary', 'words', 'dog'): doc2
    })

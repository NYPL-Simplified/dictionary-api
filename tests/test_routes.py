from flask import (
  Response,
  jsonify,
  json
)
from flask_babel import lazy_gettext as _
from nose.tools import (
    eq_,
    set_trace,
)
from api import routes
from .test_controller import TestController

class TestRoutes(TestController):
  def setup(self):
    super(TestRoutes, self).setup()

    self.test_client = self.app.test_client(self)
    self.routes = routes
    self.resolver = self.app.url_map.bind('', '/')

  def request(self, url, method='GET'):
    # Simulate a request to a URL without triggering any code outside
    # routes.py. Borrowed from circulation.

    function_name, kwargs = self.resolver.match(url, method)
    # Locate the corresponding function
    mock_function = getattr(self.routes, function_name)

    # Call it in the context of the mock app.
    with self.app.test_request_context():
      return mock_function(**kwargs)

  def test_definition(self):
    url = '/cat/definition/english/'

    response = self.request(url)
    data = json.loads(response.data)

    eq_(data['metadata']['name'], 'cat')
    eq_(data['definitions'], [
      {"metadata": "feline", "tags": [], "pos": None},
      {"metadata": "domestic animal", "tags": [], "pos": None}
    ])
    assert response.status_code == 200


    url = '/dictionary/definition/english/'

    response = self.request(url)
    data = json.loads(response.data)

    eq_(data['metadata']['name'], 'dictionary')
    eq_(data['definitions'], [
        {"metadata": "To look up in a dictionary.", 'pos': 'verb', "tags": ["transitive"]},
        {"metadata": "To add to a dictionary.", 'pos': 'verb', "tags": ["transitive"]},
        {"metadata": "To compile a dictionary.", 'pos': 'verb', "tags": ["rare", "intransitive"]},
        {"metadata": "To appear in a dictionary.", 'pos': 'verb', "tags": ["intransitive"]}
      ]
    )
    assert response.status_code == 200


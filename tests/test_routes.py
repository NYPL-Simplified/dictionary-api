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

    eq_(data['word'], 'cat')
    eq_(data['definitions'], [{"glosses": ["feline"]}, {"glosses": ["domestic animal"]}])
    assert response.status_code == 200


    url = '/dictionary/definition/english/'

    response = self.request(url)
    data = json.loads(response.data)

    eq_(data['word'], 'dictionary')
    eq_(data['definitions'], [
        {"glosses": ["To look up in a dictionary."], "tags": ["transitive"]},
        {"glosses": ["To add to a dictionary."], "tags": ["transitive"]},
        {"glosses": ["To compile a dictionary."], "tags": ["rare", "intransitive"]},
        {"glosses": ["To appear in a dictionary."], "tags": ["intransitive"]}
      ]
    )
    assert response.status_code == 200


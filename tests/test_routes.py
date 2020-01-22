from flask import (
  Response,
  jsonify,
  json
)
from flask_babel import lazy_gettext as _
from nose.tools import (
    assert_raises,
    eq_,
    set_trace,
)

from api.controller import (
  Manager,
  setup_controllers,
)
from api import routes
from .test_controller import TestController

class TestIndex(TestController):
  def setup(self):
    super(TestIndex, self).setup()

    self.test_client = self.app.test_client(self)
    self.routes = routes
    self.resolver = self.app.url_map.bind('', '/')

  def request(self, url, method='GET'):
    """Simulate a request to a URL without triggering any code outside
    routes.py. Borrowed from circulation.
    """
    function_name, kwargs = self.resolver.match(url, method)
    # Locate the corresponding function
    mock_function = getattr(self.routes, function_name)

    # Call it in the context of the mock app.
    with self.app.test_request_context():
      return mock_function(**kwargs)

  def test_definition(self):
    url = '/test/definition/english/'

    response = self.request(url)
    data = json.loads(response.data)

    eq_(data['word'], 'test')
    eq_(data['definitions'], [
      dict(glosses=["first definition"]),
      dict(glosses=["second definition"], tags=["transitive"])
    ])
    assert response.status_code == 200


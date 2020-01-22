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

from .test_controller import TestController

class TestIndex(TestController):

  def test_definition(self):
    test_client = self.app.test_client(self)
    url = '/test/definition/english/'
    
    response = test_client.get(url)
    data = json.loads(response.data)

    eq_(data['word'], 'test')
    eq_(data['definitions'], [
      dict(glosses=["first definition"]),
      dict(glosses=["second definition"], tags=["transitive"])
    ])
    assert response.status_code == 200


import endpoints
from google.appengine.ext import testbed
import webtest
import unittest
from service import SuggestionAPI
from jwt import JWT


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        tb = testbed.Testbed()
        tb.setup_env(current_version_id='testbed.version')
        tb.activate()
        tb.init_all_stubs()
        self.testbed = tb

    def tearDown(self):
        self.testbed.deactivate()

    def test_endpoint_insert(self):
        app = endpoints.api_server([SuggestionAPI], restricted=False)
        testapp = webtest.TestApp(app)
        token = JWT.create_token('user@example.com', "insert")
        testapp.authorization = ('Bearer', token)
        msg = {'title': 'Hello'}
        resp = testapp.post_json('/_ah/api/suggestion/v1/suggestion', msg)

        self.assertEqual(resp.json, {'title': 'Hello'})

    def test_endpoint_no_authorization(self):
        app = endpoints.api_server([SuggestionAPI], restricted=False)
        testapp = webtest.TestApp(app)
        token = JWT.create_token('user@example.com', "nope")
        testapp.authorization = ('Bearer', token)
        msg = {'title': 'Hello'}
        try:
            testapp.post_json('/_ah/api/suggestion/v1/suggestion', msg)
        except:
            pass

if __name__ == '__main__':
    unittest.main()

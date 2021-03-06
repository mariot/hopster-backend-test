import unittest

from google.appengine.api import users
from google.appengine.ext import testbed


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_user_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def loginUser(self, email='user@example.com', id='123', is_admin=False):
        self.testbed.setup_env(
            user_email=email,
            user_id=id,
            user_is_admin='1' if is_admin else '0',
            overwrite=True)

    def testLogin(self):
        self.assertFalse(users.get_current_user())
        self.loginUser()
        self.assertEquals(users.get_current_user().email(), 'user@example.com')
        self.loginUser(is_admin=True)
        self.assertTrue(users.is_current_user_admin())

    def testFakeLogin(self):
        self.assertFalse(users.get_current_user())
        self.loginUser(email='admin@example.com', id='321', is_admin=True)
        self.assertNotEqual(users.get_current_user().email(), 'us@example.com')
        self.assertTrue(users.is_current_user_admin())


if __name__ == '__main__':
    unittest.main()

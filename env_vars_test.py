import os
import unittest

from google.appengine.ext import testbed


class EnvVarsTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(
            app_id='hopster-backend-test',
            my_config_setting='example',
            overwrite=True)

    def tearDown(self):
        self.testbed.deactivate()

    def testEnvVars(self):
        self.assertEqual(os.environ['APPLICATION_ID'], 'hopster-backend-test')
        self.assertEqual(os.environ['MY_CONFIG_SETTING'], 'example')


if __name__ == '__main__':
    unittest.main()

import unittest

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from service import SuggestionModel


class TestEntityGroupRoot(ndb.Model):
    """Entity group root"""
    pass


def GetEntityViaMemcache(entity_key):
    """Get entity from memcache if available, from datastore if not."""
    entity = memcache.get(entity_key)
    if entity is not None:
        return entity
    key = ndb.Key(urlsafe=entity_key)
    entity = key.get()
    if entity is not None:
        memcache.set(entity_key, entity)
    return entity


class DatastoreTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def testInsertEntity(self):
        SuggestionModel().put()
        self.assertEqual(1, len(SuggestionModel.query().fetch(2)))

    def testFilterByNumber(self):
        root = TestEntityGroupRoot(id="root")
        SuggestionModel(parent=root.key).put()
        SuggestionModel(title='Hello', parent=root.key).put()
        query = SuggestionModel.query(ancestor=root.key).filter(
            SuggestionModel.title == 'Hello')
        results = query.fetch(2)
        self.assertEqual(1, len(results))
        self.assertEqual('Hello', results[0].title)

    def testGetEntityViaMemcache(self):
        entity_key = SuggestionModel(title='Hola').put().urlsafe()
        retrieved_entity = GetEntityViaMemcache(entity_key)
        self.assertNotEqual(None, retrieved_entity)
        self.assertEqual('Hola', retrieved_entity.title)

from google.appengine.datastore import datastore_stub_util  # noqa


class HighReplicationTestCaseOne(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
            probability=0)
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def testEventuallyConsistentGlobalQueryResult(self):
        class SuggestionModel(ndb.Model):
            pass

        user_key = ndb.Key('User', 'ryan')

        ndb.put_multi([
            SuggestionModel(parent=user_key),
            SuggestionModel(parent=user_key)
        ])

        self.assertEqual(0, SuggestionModel.query().count(3))
        self.assertEqual(2, SuggestionModel.query(ancestor=user_key).count(3))

    def testDeterministicOutcome(self):
        self.policy.SetProbability(.5)
        self.policy.SetSeed(2)

        class SuggestionModel(ndb.Model):
            pass

        SuggestionModel().put()

        self.assertEqual(0, SuggestionModel.query().count(3))
        self.assertEqual(0, SuggestionModel.query().count(3))
        self.assertEqual(1, SuggestionModel.query().count(3))


if __name__ == '__main__':
    unittest.main()

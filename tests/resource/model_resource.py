"""
Created on May 14, 2014

.. moduleauthor:: Peter Morihladko <morihladko@atteq.com>
"""
from unittest import TestCase

from zsl import Zsl
from zsl.resource.model_resource import ModelResource
from tests.resource.resource_test_helper import DummyModel,\
    create_resource_test_data, dummies, DummyTuple, DummyAppModel,\
    test_settings


class TestRestResource(ModelResource):
    __model__ = DummyModel


class ModelResourceTest(TestCase):
    def setUp(self):
        Zsl(__name__, config_object=test_settings)
        create_resource_test_data()

    def _testAppModel(self, dummy, model, msg=None):
        # type: (DummyTuple, DummyAppModel, str) -> None

        self.assertEqual(dummy.id, model.id, msg)
        self.assertEqual(dummy.val, model.val, msg)

    def testReadOne(self):
        resource = TestRestResource()

        test_dummy = dummies[0]
        dummy = resource.read(test_dummy.id)

        self._testAppModel(test_dummy, dummy, "read one")

    def testReadListAll(self):
        resource = TestRestResource()

        res_dummies = resource.read()

        self.assertEqual(len(dummies), len(res_dummies), "list length")

        for i, d in enumerate(res_dummies):
            self._testAppModel(dummies[i], d, "list item")

    def testCreate(self):
        resource = TestRestResource()

        dummy_data = {'val': 'eleven'}

        dummy_result = resource.create(params=None, args={}, data=dummy_data)

        dummy = resource.read(dummy_result.get_id())

        self.assertEqual(dummy_data['val'], dummy.val)

    def testUpdateOne(self):
        resource = TestRestResource()
        updated_value = 'updated'

        dummy = resource.read().pop()

        resource.update(params=dummy.get_id(), args={}, data={'val': updated_value})

        dummy = resource.read(dummy.get_id())

        self.assertEqual(updated_value, dummy.val)

    def testUpdateAll(self):
        resource = TestRestResource()

        updated_values = [DummyTuple(id=1, val='updated_1'), DummyTuple(id=2, val='updated_2')]

        resource.update(params=None, args={}, data=[x._asdict() for x in updated_values])

        for dt in updated_values:
            self._testAppModel(dt, resource.read(dt.id))

    def testDeleteOne(self):
        resource = TestRestResource()

        dummy = resource.read().pop()

        resource.delete(dummy.get_id(), args={}, data=None)

        res_dummies = resource.read()

        self.assertEqual(len(dummies) - 1, len(res_dummies))

    def testDeleteAll(self):
        resource = TestRestResource()

        resource.delete(params=None, args={}, data=None)

        res_dummies = resource.read()

        self.assertEqual(0, len(res_dummies))

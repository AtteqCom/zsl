"""
Created on May 14, 2014

.. moduleauthor:: Peter Morihladko <morihladko@atteq.com>
"""
from zsl.unittest import TestCase

from zsl.resource.model_resource import ModelResource
from tests.resource.resource_test_helper import DummyModel, create_resource_test_data


class TestModelResource(TestCase):

    @classmethod
    def setUpClass(cls):
        create_resource_test_data()

    def setUp(self):
        self.resource = service_application._injector.create_object(ModelResource, {'model_cls': DummyModel})

    def testRead(self):
        m = self.resource.read('9')
        self.assertEqual('nine', m.val, "Read one")

        m = self.resource.read(args={'limit': 'unlimited'})
        self.assertEqual(10, len(m), "We created 10 dummy models")

"""
Created on May 14, 2014

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from zsl.unittest import TestCase

from sqlalchemy.ext.declarative import declarative_base

from zsl.application.service_application import service_application
from zsl.resource.model_resource import ModelResource, ReadOnlyResourceUpdateOperationException, ReadOnlyResourceMixin
from tests.resource.resource_test_helper import create_resource_test_data, DummyModel

Base = declarative_base()


class ReadOnlyModelResource(ReadOnlyResourceMixin, ModelResource):

    pass


class TestReadOnlyModelResource(TestCase):

    @classmethod
    def setUpClass(cls):
        create_resource_test_data()

    def setUp(self):
        self.resource = service_application._injector.create_object(ReadOnlyModelResource, {'model_cls': DummyModel})

    def testRead(self):
        m = self.resource.read([9])
        self.assertEqual('nine', m.val, "Read one")
        self.assertEqual(10, len(self.resource.read([])), 'Expecting 10 dummy models.')

    def testCreate(self):
        self.assertRaises(ReadOnlyResourceUpdateOperationException, lambda: self.resource.create({}, {}, {}))

    def testDelete(self):
        self.assertRaises(ReadOnlyResourceUpdateOperationException, lambda: self.resource.delete({}, {}, {}))

    def testUpdate(self):
        self.assertRaises(ReadOnlyResourceUpdateOperationException, lambda: self.resource.update({}, {}, {}))

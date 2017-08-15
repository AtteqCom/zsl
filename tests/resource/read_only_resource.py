"""
Created on May 14, 2014

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from resource.resource_test_helper import UserModel, create_resource_test_data
from unittest.case import TestCase

from injector import inject
from sqlalchemy.ext.declarative import declarative_base

from zsl import Zsl, inject
from zsl.resource.model_resource import ModelResource, ReadOnlyResourceMixin, ReadOnlyResourceUpdateOperationException
from zsl.testing.db import DbTestCase

Base = declarative_base()


class ReadOnlyModelResource(ReadOnlyResourceMixin, ModelResource):

    pass


class TestReadOnlyModelResource(TestCase, DbTestCase):

    @classmethod
    def setUpClass(cls):
        create_resource_test_data()

    @inject(app=Zsl)
    def setUp(self, app):
        self.resource = app._injector.create_object(ReadOnlyModelResource, {'model_cls': UserModel})

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

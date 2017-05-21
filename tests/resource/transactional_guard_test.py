"""
Test the `transactional_guard` decorator in terms of creating the transaction 
before checking the policies and calling rollback if policy is broken.  
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

try:
    import unittest.mock as mock
except ImportError:
    import mock

from unittest import TestCase

from sqlalchemy.orm import Session

from zsl import Zsl
from zsl.application.containers.web_container import WebContainer
from zsl.resource.model_resource import ModelResource
from zsl.resource.guard import transactional_guard, GuardedMixin, \
    ResourcePolicy

from tests.resource.resource_test_helper import test_settings, UserModel, \
    create_resource_test_data, users


class UserResource(ModelResource):
    __model__ = UserModel


class TransactionalGuardTest(TestCase):
    def setUp(self):
        zsl = Zsl(__name__, config_object=test_settings,
                  modules=WebContainer.modules())
        zsl.testing = True

        create_resource_test_data()

    def testIsInTransaction(self):
        test_case = self

        class AllowPolicy(ResourcePolicy):
            default = True

        @transactional_guard([AllowPolicy()])
        class GuardedUserModel(UserResource, GuardedMixin):
            def update(self):
                test_case.assertIsNotNone(self._orm)
                test_case.assertTrue(self._in_transaction)

        resource = GuardedUserModel()
        user = resource.read('1', {}, {})

        self.assertDictEqual(users[0]._asdict(), user.get_attributes(),
                             "should return firs user")

    @staticmethod
    def testRollbackBefore():
        class DenyPolicy(ResourcePolicy):
            default = False

        @transactional_guard([DenyPolicy()])
        class GuardedUserModel(UserResource, GuardedMixin):
            pass

        def get_orm_mock():
            return mock.MagicMock(spec=Session)

        resource = GuardedUserModel()
        resource._session_holder = get_orm_mock
        resource.read('', {}, {})

        resource._orm.rollback.assert_called()
        resource._orm.query.assert_not_called()

    @staticmethod
    def testRollbackAfter():
        class DenyAfterPolicy(ResourcePolicy):
            default = True

            def can_read__after(self, *args, **kwargs):
                return False

        @transactional_guard([DenyAfterPolicy()])
        class GuardedUserModel(UserResource, GuardedMixin):
            pass

        def get_orm_mock():
            return mock.MagicMock(spec=Session)

        resource = GuardedUserModel()
        resource._session_holder = get_orm_mock
        resource.read('', {}, {})

        resource._orm.query.assert_called()
        resource._orm.rollback.assert_called()


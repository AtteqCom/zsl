"""
Test the `transactional_guard` decorator in terms of creating the transaction
before checking the policies and calling rollback if policy is broken.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
from resource.resource_test_helper import UserModel, create_resource_test_data, users
from unittest import TestCase

from mocks import mock_db_session

from zsl import Zsl
from zsl.application.containers.web_container import WebContainer
from zsl.application.modules.alchemy_module import TransactionHolder
from zsl.resource.guard import Access, GuardedMixin, ResourcePolicy, transactional_guard
from zsl.resource.model_resource import ModelResource
from zsl.testing.db import IN_MEMORY_DB_SETTINGS, DbTestCase

try:
    import unittest.mock as mock
except ImportError:
    import mock





class UserResource(ModelResource):
    __model__ = UserModel


class TransactionalGuardTest(TestCase):
    def setUp(self):
        zsl = Zsl(__name__, config_object=IN_MEMORY_DB_SETTINGS,
                  modules=WebContainer.modules())
        zsl.testing = True

        create_resource_test_data()
        super(TransactionalGuardTest, self).setUp()

    def testIsInTransaction(self):
        test_case = self

        class AllowPolicy(ResourcePolicy):
            default = Access.ALLOW

        @transactional_guard([AllowPolicy()])
        class GuardedUserModel(UserResource, GuardedMixin):
            def secure_read(self, *args, **kwargs):
                test_case.assertIsNotNone(self._orm)
                test_case.assertTrue(self._in_transaction)

                return super(GuardedUserModel, self).read(*args, **kwargs)

        resource = GuardedUserModel()
        user = resource.read('1', {}, {})

        self.assertDictEqual(users[0]._asdict(), user.get_attributes(),
                             "should return firs user")

    @staticmethod
    def testRollbackBefore():
        class DenyPolicy(ResourcePolicy):
            default = Access.DENY

        @transactional_guard([DenyPolicy()])
        class GuardedUserModel(UserResource, GuardedMixin):
            pass

        class TestTHolder(TransactionHolder):
            rollback = mock.MagicMock()
            _orm = mock.MagicMock()

        with mock.patch(
            'zsl.application.modules.alchemy_module.TransactionHolder',
            side_effect=TestTHolder
        ):
            resource = GuardedUserModel()
            resource.read('', {}, {})

        TestTHolder.rollback.assert_called()
        TestTHolder._orm.assert_not_called()

    @staticmethod
    def testRollbackAfter():
        class DenyAfterPolicy(ResourcePolicy):
            default = Access.ALLOW

            def can_read__after(self, *args, **kwargs):
                return Access.DENY

        mock_sess = mock_db_session()

        @transactional_guard([DenyAfterPolicy()])
        class GuardedUserModel(UserResource, GuardedMixin):
            pass

        class MyTestCase(DbTestCase, TestCase):
            def runTest(self):
                pass

            def testIt(self):
                resource = GuardedUserModel()
                resource.read('', {}, {})

                mock_sess.query.assert_called()
                mock_sess.rollback.assert_called()

        test_case = MyTestCase()
        test_case.setUp()
        test_case.testIt()
        test_case.tearDown()

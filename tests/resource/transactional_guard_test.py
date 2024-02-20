"""
Test the `transactional_guard` decorator in terms of creating the transaction
before checking the policies and calling rollback if policy is broken.
"""
from resource.resource_test_helper import UserModel, create_resource_test_data, users
from unittest import TestCase
import unittest.mock as mock

from mocks import mock_db_session
import sqlalchemy.engine

from zsl import Injected, Zsl, inject
from zsl.application.containers.web_container import WebContainer
from zsl.application.modules.alchemy_module import TransactionHolder
from zsl.resource.guard import Access, GuardedMixin, ResourcePolicy, transactional_guard
from zsl.resource.model_resource import ModelResource
from zsl.testing.db import IN_MEMORY_DB_SETTINGS, DbTestCase, TestSessionFactory


class UserResource(ModelResource):
    __model__ = UserModel


class TransactionalGuardTest(TestCase):
    @inject(engine=sqlalchemy.engine.Engine)
    def setUp(self, engine = Injected):
        zsl = Zsl(__name__, config_object=IN_MEMORY_DB_SETTINGS,
                  modules=WebContainer.modules())
        zsl.testing = True
        TestSessionFactory.reset_db_schema_initialization(engine)

        super().setUp()

    @inject(engine=sqlalchemy.engine.Engine)
    def tearDown(self, engine=Injected):
        super(TransactionalGuardTest, self).tearDown()
        TestSessionFactory.reset_db_schema_initialization(engine)

    def testIsInTransaction(self):
        test_case = self

        class AllowPolicy(ResourcePolicy):
            default = Access.ALLOW

        @transactional_guard([AllowPolicy()])
        class GuardedUserModel(UserResource, GuardedMixin):
            def secure_read(self, *args, **kwargs):
                test_case.assertIsNotNone(self._orm)
                test_case.assertTrue(self._in_transaction)

                return super().read(*args, **kwargs)

        create_resource_test_data()

        resource = GuardedUserModel()
        user = resource.read('1', {}, {})

        self.assertDictEqual(users[0]._asdict(), user.get_attributes(),
                             "should return first user")

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

        create_resource_test_data()
        with mock.patch(
            'zsl.application.modules.alchemy_module.TransactionHolder',
            side_effect=TestTHolder
        ):
            resource = GuardedUserModel()
            resource.read('', {}, {})

        TestTHolder.rollback.assert_called_with()
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
                create_resource_test_data()
                resource = GuardedUserModel()
                resource.read('', {}, {})

                if hasattr(mock_sess.query, 'assert_called'):
                    mock_sess.query.assert_called()
                mock_sess.rollback.assert_called_with()

        test_case = MyTestCase()
        test_case.setUp()
        test_case.testIt()
        test_case.tearDown()

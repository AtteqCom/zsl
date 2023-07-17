from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
from unittest.case import TestCase
from unittest.mock import call

from mocks import mock, mock_db_session
from sqlalchemy.orm.session import Session

from zsl import inject
from zsl.application.containers.container import IoCContainer
from zsl.application.modules.alchemy_module import AlchemyModule
from zsl.application.modules.context_module import DefaultContextModule
from zsl.application.modules.logger_module import LoggerModule
from zsl.application.modules.task_router import TaskRouterModule
from zsl.service.service import SessionFactory
from zsl.testing.db import IN_MEMORY_DB_SETTINGS, DbTestCase, DbTestModule
from zsl.testing.db import TestSessionFactory as SessionFactoryForTesting
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration
from zsl.utils.injection_helper import bind


class TestContainerNoTestSessionFactory(IoCContainer):
    logger = LoggerModule
    database = AlchemyModule
    context = DefaultContextModule
    task_router = TaskRouterModule


class TestContainerTestSessionFactory(TestContainerNoTestSessionFactory):
    session_factory = DbTestModule


class DbTestCaseTest(ZslTestCase, TestCase):
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name="TestSessionFactoryTest",
        config_object=IN_MEMORY_DB_SETTINGS,
        container=TestContainerNoTestSessionFactory
    )

    class DbTest(DbTestCase, TestCase):
        def runTest(self):
            pass

    class AnotherDbTest(DbTestCase, TestCase):
        def runTest(self):
            pass

    def test_db_test_case(self):
        test = DbTestCaseTest.DbTest()
        with mock.patch('zsl.testing.db.metadata') as mock_metadata:
            mock_sess = mock_db_session()
            test.setUp()
            test.tearDown()
            mock_sess.begin_nested.assert_called_once_with()
            mock_sess.rollback.assert_called_once_with()
            mock_sess.close.assert_called_once_with()

    def test_db_test_case_session(self):
        test = DbTestCaseTest.DbTest()
        mock_tsf = mock.MagicMock()
        bind(SessionFactoryForTesting, to=mock_tsf)
        test.setUp()
        mock_tsf.create_test_session.assert_called_once_with()
        mock_tsf.create_session.assert_not_called()

    def test_db_schema_is_recreated_exactly_once_within_run_of_all_tests(self):
        # unfortunately we have to reset the db schema initialization to be able to test, if the schema is correctly
        # initialized. The reason is that the class `SessionFactoryForTesting` is also used in another tests and the
        # schema could already be initialized when running these tests.
        SessionFactoryForTesting.reset_db_schema_initialization()

        test_1 = DbTestCaseTest.DbTest()
        test_2 = DbTestCaseTest.AnotherDbTest()
        with mock.patch('zsl.testing.db.metadata') as mock_metadata:
            mock_db_session()
            test_1.setUp()
            test_1.tearDown()
            test_1.setUp()
            test_1.tearDown()
            test_2.setUp()
            test_2.tearDown()
            mock_metadata.drop_all.assert_called_once_with(mock_metadata.bind)
            mock_metadata.create_all.assert_called_once_with(mock_metadata.bind)
            # checking whether drop_all is called before create_all
            mock_metadata.assert_has_calls(
                [call.drop_all(mock_metadata.bind), call.create_all(mock_metadata.bind)], any_order=False
            )


class TestSessionFactoryTest(ZslTestCase, TestCase):
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name="TestSessionFactoryTest",
        config_object=IN_MEMORY_DB_SETTINGS,
        container=TestContainerNoTestSessionFactory
    )

    def test_single_session(self):
        self.assertNotEqual(SessionFactoryForTesting(), SessionFactoryForTesting(),
                            "Two different instances may not be equal.")

        f = SessionFactoryForTesting()
        f.create_test_session()
        self.assertEqual(f.create_session(), f.create_session(),
                         "Two results must be equal.")

        self.assertIsInstance(f.create_session(), Session, "Session must be correct.")


class DbTestModuleTest(ZslTestCase, TestCase):
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name="DbTestModuleTest",
        config_object=IN_MEMORY_DB_SETTINGS,
        container=TestContainerTestSessionFactory
    )

    def test_test_session_factory_is_injected(self):
        @inject(session_factory=SessionFactory)
        def get_session_factory(session_factory):
            return session_factory

        @inject(test_session_factory=SessionFactoryForTesting)
        def get_test_session_factory(test_session_factory):
            return test_session_factory

        self.assertIsInstance(get_session_factory(), SessionFactoryForTesting,
                              "Correct session factory must be returned")

        self.assertIsInstance(get_test_session_factory(),
                              SessionFactoryForTesting,
                              "Correct session factory must be returned")

        self.assertEqual(get_test_session_factory(), get_session_factory(),
                         "Test session factory and session factory must "
                         "be the same")

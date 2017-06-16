from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from builtins import *

from unittest.case import TestCase

from sqlalchemy.orm.session import Session

from mocks import mock_db_session, mock
from zsl.application.containers.container import IoCContainer
from zsl.application.modules.alchemy_module import AlchemyModule
from zsl.application.modules.context_module import DefaultContextModule
from zsl.application.modules.logger_module import LoggerModule
from zsl.application.modules.task_router import TaskRouterModule
from zsl.service.service import SessionFactory
from zsl.testing.db import TestSessionFactory, DbTestModule, DbTestCase, IN_MEMORY_DB_SETTINGS
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration
from zsl import inject
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

    def test_db_test_case(self):
        test = DbTestCaseTest.DbTest()
        with mock.patch('zsl.testing.db.metadata') as mock_metadata:
            mock_sess = mock_db_session()
            DbTestCaseTest.DbTest.setUpClass()
            mock_metadata.create_all.assert_called_once()
            test.setUp()
            test.tearDown()
            mock_sess.rollback.assert_called_once()
            mock_sess.close.assert_called_once()
            mock_sess.reset_mock()
            DbTestCaseTest.DbTest.tearDownClass()
            mock_sess.rollback.assert_called_once()
            mock_sess.close.assert_called_once()

    def test_db_test_case_session(self):
        test = DbTestCaseTest.DbTest()
        mock_tsf = mock.MagicMock()
        bind(TestSessionFactory, to=mock_tsf)
        DbTestCaseTest.DbTest.setUpClass()
        mock_tsf.create_session.assert_called_once()
        mock_tsf.reset_mock()
        test.setUp()
        mock_tsf.create_session.assert_called_once()


class TestSessionFactoryTest(ZslTestCase, TestCase):
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name="TestSessionFactoryTest",
        config_object=IN_MEMORY_DB_SETTINGS,
        container=TestContainerNoTestSessionFactory
    )

    def test_single_session(self):
        self.assertNotEquals(TestSessionFactory(), TestSessionFactory(),
                             "Two different instances may not be equal.")

        f = TestSessionFactory()
        self.assertEquals(f.create_session(), f.create_session(),
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

        @inject(test_session_factory=TestSessionFactory)
        def get_test_session_factory(test_session_factory):
            return test_session_factory

        self.assertIsInstance(get_session_factory(), TestSessionFactory,
                              "Correct session factory must be returned")

        self.assertIsInstance(get_test_session_factory(), TestSessionFactory,
                              "Correct session factory must be returned")

        self.assertEquals(get_test_session_factory(), get_session_factory(),
                          "Test session factory and session factory must "
                          "be the same")


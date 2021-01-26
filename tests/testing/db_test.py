from unittest.case import TestCase

from mocks import mock, mock_db_session
from sqlalchemy.orm.session import Session

from zsl import Zsl, inject
from zsl.application.containers.container import IoCContainer
from zsl.application.modules.alchemy_module import AlchemyModule
from zsl.application.modules.context_module import DefaultContextModule
from zsl.application.modules.logger_module import LoggerModule
from zsl.application.modules.task_router import TaskRouterModule
from zsl.service.service import SessionFactory
from zsl.testing.db import IN_MEMORY_DB_SETTINGS, DbTestCase, DbTestModule
from zsl.testing.db import TestSessionFactory as SessionFactoryForTesting
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration


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
            test.setUp()
            test.tearDown()
            mock_metadata.create_all.assert_called_once_with(mock_metadata.bind)
            mock_sess.begin_nested.assert_called_once_with()
            mock_sess.rollback.assert_called_once_with()
            mock_sess.close.assert_called_once_with()

    @inject
    def test_db_test_case_session(self, app: Zsl):
        test = DbTestCaseTest.DbTest()
        mock_tsf = mock.MagicMock()
        app.injector.binder.bind(SessionFactoryForTesting, to=mock_tsf)
        test.setUp()
        mock_tsf.create_test_session.assert_called_once_with()
        mock_tsf.create_session.assert_not_called()


class TestSessionFactoryTest(ZslTestCase, TestCase):
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name="TestSessionFactoryTest",
        config_object=IN_MEMORY_DB_SETTINGS,
        container=TestContainerNoTestSessionFactory
    )

    @inject
    def test_single_session(self, app: Zsl) -> None:
        # This tests that two calls do constructor create different objects and no unexpected singletons are crated.
        self.assertNotEqual(app.injector.create_object(SessionFactoryForTesting),
                            app.injector.create_object(SessionFactoryForTesting),
                            "Two different instances may not be equal.")

        f = app.injector.create_object(SessionFactoryForTesting)
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

    @inject
    def test_test_session_factory_is_injected(self, app: Zsl):
        def get_session_factory() -> SessionFactory:
            return app.injector.get(SessionFactory)

        def get_test_session_factory() -> SessionFactoryForTesting:
            return app.injector.get(SessionFactoryForTesting)

        self.assertIsInstance(get_session_factory(), SessionFactoryForTesting,
                              "Correct session factory must be returned")

        self.assertIsInstance(get_test_session_factory(),
                              SessionFactoryForTesting,
                              "Correct session factory must be returned")

        self.assertEqual(get_test_session_factory(), get_session_factory(),
                         "Test session factory and session factory must "
                         "be the same")

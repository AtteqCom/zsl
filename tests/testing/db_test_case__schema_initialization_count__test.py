from unittest import mock
from unittest.case import TestCase
from unittest.mock import call

from zsl.application.containers.container import IoCContainer
from zsl.application.modules.alchemy_module import AlchemyModule
from zsl.application.modules.context_module import DefaultContextModule
from zsl.application.modules.logger_module import LoggerModule
from zsl.application.modules.task_router import TaskRouterModule
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


class DbTestCase_SchemaInitializationCount_Test(ZslTestCase, TestCase):
    """Test that the schema is initialized exactly once within the run of all tests."""

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

    def test_db_schema_is_recreated_exactly_once_within_run_of_all_tests(self):
        # unfortunately we have to reset the db schema initialization to be able to test, if the schema is correctly
        # initialized. The reason is that the class `SessionFactoryForTesting` is also used in another tests and the
        # schema could already be initialized when running these tests.
        SessionFactoryForTesting.reset_db_schema_initialization()

        test_1 = DbTestCase_SchemaInitializationCount_Test.DbTest()
        test_2 = DbTestCase_SchemaInitializationCount_Test.AnotherDbTest()
        with mock.patch('zsl.testing.db.metadata') as mock_metadata:
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

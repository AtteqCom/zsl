from unittest import mock
from unittest.case import TestCase

import sqlalchemy
from sqlalchemy import inspect, text

from zsl import Injected, inject
from zsl.application.containers.container import IoCContainer
from zsl.application.modules.alchemy_module import AlchemyModule, EnginePool
from zsl.application.modules.context_module import DefaultContextModule
from zsl.application.modules.logger_module import LoggerModule
from zsl.application.modules.task_router import TaskRouterModule
from zsl.db.model.sql_alchemy import DeclarativeBase, metadata
from zsl.service import transactional, use_db_master_node
from zsl.service.service import TransactionalSupportMixin
from zsl.testing.db import IN_MEMORY_DB_SETTINGS, DatabaseSchemaInitializationException, DbTestCase, DbTestModule
from zsl.testing.db import TestSessionFactory as SessionFactoryForTesting
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration


class TestContainerNoTestSessionFactory(IoCContainer):
    logger = LoggerModule
    database = AlchemyModule
    context = DefaultContextModule
    task_router = TaskRouterModule


class TestContainerTestSessionFactory(TestContainerNoTestSessionFactory):
    session_factory = DbTestModule


class DbTestCase_SchemaInitializationAndQuerying_Test(ZslTestCase, TestCase):
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name="DbTestModuleTest",
        config_object=IN_MEMORY_DB_SETTINGS,
        container=TestContainerTestSessionFactory
    )

    # see `setUpClass` for definition of the Foo model
    _FOO_MODEL = None

    class DbTest1(DbTestCase, TransactionalSupportMixin, TestCase):

        @transactional
        def test_select_record_by_name_from_foo(self):
            return (
                self._orm.query(DbTestCase_SchemaInitializationAndQuerying_Test._FOO_MODEL)
                .filter(DbTestCase_SchemaInitializationAndQuerying_Test._FOO_MODEL.name == "test")
                .first()
            )

        @transactional
        def test_select_count_from_foo(self) -> int:
            return self._orm.query(DbTestCase_SchemaInitializationAndQuerying_Test._FOO_MODEL).count()

        @transactional
        def test_insert_into_foo_and_select_count(self):
            foo = DbTestCase_SchemaInitializationAndQuerying_Test._FOO_MODEL()
            foo.name = "test"
            self._orm.add(foo)
            self._orm.flush()
            count = self._orm.query(DbTestCase_SchemaInitializationAndQuerying_Test._FOO_MODEL).count()
            return count

        @use_db_master_node
        def test_insert_into_foo_and_select_count__with_use_db_master_node(self):
            return self.test_insert_into_foo_and_select_count()

    class DbTest2(DbTest1):
        pass

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # we are defining our Foo model in the setUpClass method in order to have control over Foo "registration" to
        # the global object `zsl.db.model.sql_alchemy.metadata`. We don't want the Foo model to be registered to the
        # global object outside the scope of this test class - it could cause problems in other tests.
        class Foo(DeclarativeBase):
            __tablename__ = 'foo'
            id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
            name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

        cls._FOO_MODEL = Foo

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        # removing our Foo model from the global object `zsl.db.model.sql_alchemy.metadata`
        metadata.remove(cls._FOO_MODEL.__table__)

        cls._FOO_MODEL = None

    @inject(engine_pool=EnginePool)
    def setUp(self, engine_pool=Injected):
        super().setUp()
        # unfortunately we have to reset the db schema initialization to be able to test, if the schema is correctly
        # initialized. The reason is that the class `SessionFactoryForTesting` is also used in another tests and the
        # schema could already be initialized when running these tests.
        SessionFactoryForTesting.reset_db_schema_initialization(engine_pool.get_engine(EnginePool._DEFAULT_ENGINE_NAME))

    @inject(engine_pool=EnginePool)
    def tearDown(self, engine_pool=Injected):
        super().tearDown()
        SessionFactoryForTesting.reset_db_schema_initialization(engine_pool.get_engine(EnginePool._DEFAULT_ENGINE_NAME))

    def test_db_schema_is_created_in_setupclass(self):
        test = DbTestCase_SchemaInitializationAndQuerying_Test.DbTest1()
        with mock.patch('zsl.testing.db.metadata') as mock_metadata:
            test.setUpClass()

            mock_metadata.drop_all.assert_not_called()
            mock_metadata.create_all.assert_called_once_with(mock_metadata.bind)

    def test_db_schema_is_created_exactly_once_within_run_of_all_tests(self):
        test_1 = DbTestCase_SchemaInitializationAndQuerying_Test.DbTest1()
        test_2 = DbTestCase_SchemaInitializationAndQuerying_Test.DbTest2()
        with mock.patch('zsl.testing.db.metadata') as mock_metadata:
            test_1.setUpClass()
            test_1.setUp()
            test_1.tearDown()
            test_1.setUp()
            test_1.tearDown()
            test_1.tearDownClass()

            test_2.setUpClass()
            test_2.setUp()
            test_2.tearDown()
            test_2.tearDownClass()

            mock_metadata.drop_all.assert_not_called()
            mock_metadata.create_all.assert_called_once_with(mock_metadata.bind)

    @inject(engine_pool=EnginePool)
    def test__when_db_contains_table__then_exception_is_raised_within_setup_and_schema_is_not_created(
        self, engine_pool
    ):
        engine = engine_pool.get_engine(EnginePool._DEFAULT_ENGINE_NAME)
        # create a table in the database
        with engine.connect() as connection:
            connection.execute(text("CREATE TABLE bar (id INTEGER PRIMARY KEY, name TEXT)"))

        db_test = DbTestCase_SchemaInitializationAndQuerying_Test.DbTest1()

        # database schema initialization should fail
        with self.assertRaises(DatabaseSchemaInitializationException):
            db_test.setUpClass()

        # check that no table was created or dropped
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        self.assertEqual(existing_tables, ["bar"], "No table should be dropped or created.")

        # clean up
        with engine.connect() as connection:
            connection.execute(text("DROP TABLE bar"))

    def test_tables_exists_within_tests(self):
        db_test_1 = DbTestCase_SchemaInitializationAndQuerying_Test.DbTest1()
        db_test_2 = DbTestCase_SchemaInitializationAndQuerying_Test.DbTest2()

        try:
            db_test_1.setUpClass()
            db_test_1.setUp()
            db_test_1.test_select_record_by_name_from_foo()
            db_test_1.tearDown()

            db_test_1.setUp()
            db_test_1.test_select_count_from_foo()
            db_test_1.tearDown()
            db_test_1.tearDownClass()

            db_test_2.setUpClass()
            db_test_2.setUp()
            db_test_2.test_select_count_from_foo()
            db_test_2.tearDown()
            db_test_2.tearDownClass()
        except Exception as e:
            self.fail("Exception raised: " + str(e))

    def test_data_created_within_test_are_not_available_in_another_test(self):
        db_test = DbTestCase_SchemaInitializationAndQuerying_Test.DbTest1()

        db_test.setUpClass()

        # inserting data into foo
        db_test.setUp()
        count_in_first_test = db_test.test_insert_into_foo_and_select_count()
        db_test.tearDown()

        db_test.setUp()
        # SELECT COUNT(*) FROM foo in another test
        count_in_second_test = db_test.test_select_count_from_foo()
        db_test.tearDown()

        db_test.tearDownClass()

        self.assertEqual(count_in_first_test, 1, "There should be one row in the table foo within first test")
        self.assertEqual(count_in_second_test, 0, "There should be no rows in the table foo within second test")

    def test_created_with_different_node_context__then_data_should_be_shared(self):
        db_test = DbTestCase_SchemaInitializationAndQuerying_Test.DbTest1()

        db_test.setUpClass()

        db_test.setUp()

        # inserting data into foo in default node context
        count_in_default_node = db_test.test_insert_into_foo_and_select_count()
        count_in_master_node = db_test.test_insert_into_foo_and_select_count__with_use_db_master_node()

        db_test.tearDown()

        db_test.tearDownClass()

        self.assertEqual(count_in_default_node, 1, "There should be one row in the table foo within default node context")
        self.assertEqual(count_in_master_node, 2, "There should be two rows in the table foo within master node context")

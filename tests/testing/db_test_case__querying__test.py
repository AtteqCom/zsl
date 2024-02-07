from unittest.case import TestCase

import sqlalchemy

from zsl.application.containers.container import IoCContainer
from zsl.application.modules.alchemy_module import AlchemyModule
from zsl.application.modules.context_module import DefaultContextModule
from zsl.application.modules.logger_module import LoggerModule
from zsl.application.modules.task_router import TaskRouterModule
from zsl.db.model.sql_alchemy import DeclarativeBase, metadata
from zsl.service import transactional
from zsl.service.service import TransactionalSupportMixin
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


class DbTestCase_Querying_Test(ZslTestCase, TestCase):
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
                self._orm.query(DbTestCase_Querying_Test._FOO_MODEL)
                .filter(DbTestCase_Querying_Test._FOO_MODEL.name == "test")
                .first()
            )

        @transactional
        def test_select_count_from_foo(self) -> int:
            return self._orm.query(DbTestCase_Querying_Test._FOO_MODEL).count()

        @transactional
        def test_insert_into_foo(self):
            foo = DbTestCase_Querying_Test._FOO_MODEL()
            foo.name = "test"
            self._orm.add(foo)
            self._orm.flush()
            count = self._orm.query(DbTestCase_Querying_Test._FOO_MODEL).count()
            self.assertEqual(count, 1, "There should be one row in the table foo")

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

    def setUp(self):
        super().setUp()
        # unfortunately we have to reset the db schema initialization to be able to test, if the schema is correctly
        # initialized. The reason is that the class `SessionFactoryForTesting` is also used in another tests and the
        # schema could already be initialized when running these tests.
        SessionFactoryForTesting.reset_db_schema_initialization()

    def test_tables_exists_within_tests(self):
        db_test_1 = DbTestCase_Querying_Test.DbTest1()
        db_test_2 = DbTestCase_Querying_Test.DbTest2()

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
        db_test = DbTestCase_Querying_Test.DbTest1()

        # inserting data into foo
        db_test.setUp()
        db_test.test_insert_into_foo()
        db_test.tearDown()

        db_test.setUp()
        # SELECT COUNT(*) FROM foo in another test
        count = db_test.test_select_count_from_foo()
        db_test.tearDown()

        self.assertEqual(count, 0, "There should be no rows in the table foo within another test")

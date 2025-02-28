"""
:mod:`zsl.testing.db`
---------------------
This module allows for database unit testing. For how to use the database
testing in practice, a sample, refer to :ref:`unit-testing-db`.

The module works in the following way (methods setUp, tearDown):
1. Each test runs in a single transaction.
2. This transaction is always called a rollback.

All the tests are run in a single parent transaction (setUpClass,
tearDownClass):
1. In general initialization phase the session/transaction is created
and it is kept during all the testing. Also the database schema is created.
2. After this the transaction is called rollback.

This means that the tests may be conducted in the in the memory database
or a persistent one which is kept clean.

The module provides class :class:`.TestSessionFactory` - it always returns
the same session. Also one should add :class:`.DbTestModule` to the test
container when creating Zsl instance, see :ref:`unit-testing-zsl-instance`.
"""

import logging

from injector import Module, provides, singleton
from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session, sessionmaker

from zsl import Injected, inject
from zsl.application.modules.alchemy_module import (EnginePool, SessionHolder, TransactionHolder,
                                                    TransactionHolderFactory)
from zsl.db.model.sql_alchemy import metadata
from zsl.service.service import SessionFactory

logger = logging.getLogger(__name__)


class DatabaseSchemaInitializationException(Exception):
    pass


class TestSessionHolder(SessionHolder):
    def __init__(self, engine_pool: EnginePool):
        default_engine = engine_pool.get_engine(EnginePool._DEFAULT_ENGINE_NAME)
        super().__init__(
            sessionmaker(
                bind=default_engine,
                autocommit=False,
                expire_on_commit=False,
            )
        )


class TestSessionFactory(SessionFactory):
    """Factory always returning the single test transaction."""
    _test_session = None
    _db_schema_initialized = False

    @classmethod
    def reset_db_schema_initialization(cls, engine: Engine) -> None:
        metadata.drop_all(engine)
        cls._db_schema_initialized = False

    @inject(engine_pool=EnginePool)
    def initialize_db_schema(self, engine_pool: EnginePool = Injected) -> None:
        engine = engine_pool.get_engine(EnginePool._DEFAULT_ENGINE_NAME)
        if not TestSessionFactory._db_schema_initialized:
            logger.info("Initialize db schema")
            metadata.bind = engine

            logger.debug("Initialize db schema - Check if db contains any table.")
            self._raise_if_database_is_not_empty(engine)

            logger.debug("Initialize db schema - Create all tables.")
            metadata.create_all(engine)
            logger.debug("Initialize db schema - Create all tables - Done.")

            TestSessionFactory._db_schema_initialized = True
            logger.info("Initialize db schema - Done.")

    def create_test_session(self) -> Session:
        assert TestSessionFactory._test_session is None
        logger.debug("Create test session - begin test session/setUp")
        TestSessionFactory._test_session = self._session_holder()
        TestSessionFactory._test_session.autoflush = True
        TestSessionFactory._test_session.begin_nested()
        assert TestSessionFactory._test_session is not None
        return TestSessionFactory._test_session

    def create_session(self):
        logger.debug("Create test session")
        assert TestSessionFactory._test_session is not None
        return TestSessionFactory._test_session

    def close_test_session(self):
        TestSessionFactory._test_session.rollback()
        TestSessionFactory._test_session.close()
        TestSessionFactory._test_session = None
        logger.debug("Close test session - close test test session/tearDown")

    def _raise_if_database_is_not_empty(self, engine):
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        if len(existing_tables) > 0:
            raise DatabaseSchemaInitializationException(
                f"The database contains already some tables. This is forbidden to prevent accidentally running tests "
                f"on a production database. Database url: {engine.url}. Found tables: {existing_tables}"
            )


class TestTransactionHolder(TransactionHolder):
    def __init__(self):
        super().__init__()
        self._nested_tx = None

    def begin(self):
        self._nested_tx = self.session.begin_nested()

    def commit(self):
        self._nested_tx.commit()

    def rollback(self):
        self._nested_tx.rollback()

    def close(self):
        logger.debug("Close.")
        self._orm = None
        self._in_transaction = False


class TestTransactionHolderFactory(TransactionHolderFactory):
    def create_transaction_holder(self):
        return TestTransactionHolder()


class DbTestModule(Module):
    """Module fixing the :class:`zsl.service.service.SessionFactory`
    to our :class:`.TestSessionFactory`."""

    @provides(SessionHolder, scope=singleton)
    @inject(engine_pool=EnginePool)
    def provide_session_holder(
        self, engine_pool: EnginePool
    ) -> SessionHolder:
        return TestSessionHolder(engine_pool)

    @provides(SessionFactory, scope=singleton)
    def get_session_factory(self) -> SessionFactory:
        return TestSessionFactory()

    @provides(TestSessionFactory, scope=singleton)
    @inject(session_factory=SessionFactory)
    def get_test_session_factory(
        self, session_factory: SessionFactory = Injected
    ) -> SessionFactory:
        return session_factory

    @provides(TransactionHolderFactory, scope=singleton)
    def provide_transaction_holder_factory(self) -> TransactionHolderFactory:
        return TestTransactionHolderFactory()


class DbTestCase:
    """:class:`.DbTestCase` is a mixin to be used when testing with
    a database."""

    _session = None

    @classmethod
    @inject(session_factory=TestSessionFactory)
    def setUpClass(cls, session_factory: TestSessionFactory = Injected) -> None:
        super().setUpClass()
        session_factory.initialize_db_schema()

    @inject(session_factory=TestSessionFactory)
    def setUp(self, session_factory: TestSessionFactory = Injected) -> None:
        super().setUp()
        logger.debug("DbTestCase.setUp")
        session_factory.create_test_session()

    @inject(session_factory=TestSessionFactory)
    def tearDown(self, session_factory: TestSessionFactory = Injected) -> None:
        # This will return the same transaction/session
        # as the one used in setUp.
        logger.debug("DbTestCase.tearDown")
        session_factory.close_test_session()
        super().tearDown()


IN_MEMORY_DB_SETTINGS = {
    "DATABASE_URI": "sqlite:///:memory:",
    "DATABASE_MASTER_NODE_NAME": "master",
    "DATABASE_ENGINE_PROPS": {},
    "JSON_AS_ASCII": False,
}

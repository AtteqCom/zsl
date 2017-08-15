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
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
import logging

from injector import Module, provides, singleton
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session

from zsl import inject
from zsl.application.modules.alchemy_module import TransactionHolder, TransactionHolderFactory
from zsl.db.model.sql_alchemy import metadata
from zsl.service.service import SessionFactory


class TestSessionFactory(SessionFactory):
    """Factory always returning the single test transaction."""
    _test_session = None

    @inject(engine=Engine)
    def create_test_session(self, engine):
        # type: (Engine) -> Session
        assert TestSessionFactory._test_session is None
        metadata.bind = engine
        metadata.create_all(engine)
        logging.getLogger(__name__).debug("Create test session - begin test session/setUp")
        TestSessionFactory._test_session = self._session_holder()
        TestSessionFactory._test_session.autoflush = True
        TestSessionFactory._test_session.begin_nested()
        assert TestSessionFactory._test_session is not None
        return TestSessionFactory._test_session

    def create_session(self):
        logging.getLogger(__name__).debug("Create test session")
        assert TestSessionFactory._test_session is not None
        return TestSessionFactory._test_session

    def close_test_session(self):
        TestSessionFactory._test_session.rollback()
        TestSessionFactory._test_session.close()
        TestSessionFactory._test_session = None
        logging.getLogger(__name__).debug("Close test session - close test test session/tearDown")


class TestTransactionHolder(TransactionHolder):
    def begin(self):
        self.session.begin_nested()

    def close(self):
        logging.getLogger(__name__).debug("Close.")
        self._orm = None
        self._in_transaction = False


class TestTransactionHolderFactory(TransactionHolderFactory):
    def create_transaction_holder(self):
        return TestTransactionHolder()


class DbTestModule(Module):
    """Module fixing the :class:`zsl.service.service.SessionFactory`
    to our :class:`.TestSessionFactory`."""

    @provides(SessionFactory, scope=singleton)
    def get_session_factory(self):
        # type: ()->SessionFactory
        return TestSessionFactory()

    @provides(TestSessionFactory, scope=singleton)
    @inject(session_factory=SessionFactory)
    def get_test_session_factory(self, session_factory):
        # type: (SessionFactory)->SessionFactory
        return session_factory

    @provides(TransactionHolderFactory, scope=singleton)
    def provide_transaction_holder_factory(self):
        return TestTransactionHolderFactory()


class DbTestCase(object):
    """:class:`.DbTestCase` is a mixin to be used when testing with
    a database."""

    _session = None

    @inject(session_factory=TestSessionFactory)
    def setUp(self, session_factory):
        super(DbTestCase, self).setUp()
        # type: (TestSessionFactory)->None
        logging.getLogger(__name__).debug("DbTestCase.setUp")
        session_factory.create_test_session()

    @inject(session_factory=TestSessionFactory)
    def tearDown(self, session_factory):
        # type: (TestSessionFactory)->None
        # This will return the same transaction/session
        # as the one used in setUp.
        logging.getLogger(__name__).debug("DbTestCase.tearDown")
        session_factory.close_test_session()
        super(DbTestCase, self).tearDown()


IN_MEMORY_DB_SETTINGS = {
    'DATABASE_URI': 'sqlite:///:memory:',
    'DATABASE_ENGINE_PROPS': {},
    'JSON_AS_ASCII': False
}

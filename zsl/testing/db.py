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
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from injector import Module, provides, singleton
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session

from zsl import inject
from zsl.db.model.sql_alchemy import metadata
from zsl.service.service import SessionFactory


class TestSessionFactory(SessionFactory):
    """Factory always returning the single test transaction."""
    _test_session = None

    def __init__(self):
        super(TestSessionFactory, self).__init__()

    def create_session(self):
        # type: () -> Session
        if TestSessionFactory._test_session is None:
            TestSessionFactory._test_session = self._session_holder()

        assert TestSessionFactory._test_session is not None
        return TestSessionFactory._test_session

    def close_session(self):
        pass


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


class DbTestCase(object):
    """:class:`.DbTestCase` is a mixin to be used when testing with a database."""

    _session = None

    @classmethod
    @inject(session_factory=TestSessionFactory, engine=Engine)
    def setUpClass(cls, engine, session_factory):
        # type: (Engine, SessionFactory)->None
        super(DbTestCase, cls).setUpClass()
        DbTestCase._session = session_factory.create_session()
        metadata.bind = engine
        metadata.create_all(engine)

    @inject(session_factory=TestSessionFactory)
    def setUp(self, session_factory):
        # type: (SessionFactory)->None
        session = session_factory.create_session()
        session.begin(subtransactions=True)

    @inject(session_factory=TestSessionFactory)
    def tearDown(self, session_factory):
        # type: (SessionFactory)->None
        # This will return the same transaction/session
        # as the one used in setUp.
        sess = session_factory.create_session()
        sess.rollback()
        sess.close()

    @classmethod
    def tearDownClass(cls):
        session = DbTestCase._session
        session.rollback()
        session.close()


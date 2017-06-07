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
    @classmethod
    @inject(session_factory=TestSessionFactory, engine=Engine)
    def setUpClass(cls, engine, session_factory):
        # type: (Engine, SessionFactory)->None
        super(DbTestCase, cls).setUpClass()
        session_factory.create_session()
        metadata.bind = engine
        metadata.create_all(engine)

    @inject(session_factory=TestSessionFactory)
    def setUp(self, session_factory):
        # type: (SessionFactory)->None
        session_factory.create_session()

    @inject(session_factory=TestSessionFactory)
    def tearDown(self, session_factory):
        # type: (SessionFactory)->None
        sess = session_factory.create_session()
        sess.rollback()
        sess.close()

    @classmethod
    @inject(session_factory=TestSessionFactory)
    def tearDownClass(cls, session_factory):
        session = session_factory.create_session()
        session.rollback()
        session.close()

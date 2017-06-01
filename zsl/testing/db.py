from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoping

from zsl import inject
from zsl.application.modules.alchemy_module import SessionHolder
from zsl.db.model.sql_alchemy import metadata
from zsl.service.service import TransactionalSupport
from zsl.utils.injection_helper import bind


class TestTransactionalSupport(object):

    _test_session = None

    @inject(session_holder=SessionHolder)
    def __init__(self, session_holder):
        self._orm = None  # type: Session
        self._session_holder = session_holder

    def create_session(self):
        # type: ()->Session
        return self._session_holder()

    def close_session(self):
        pass


class DbTestCase(object):
    @classmethod
    @inject(engine=Engine)
    def setUpClass(cls, engine):
        tx_support = TransactionalSupport()
        sess = tx_support.create_session()

        metadata.bind = engine
        metadata.create_all(engine)

        sess.close()

    @inject(transactional_support=TransactionalSupport)
    def setUp(self, transactional_support):
        self._old_transactional_support = transactional_support
        # TODO: Child
        self._tx_support = TestTransactionalSupport()
        bind(TransactionalSupport, to=self._tx_support, scope=singleton)
        self._tx_support.create_session()

    def tearDown(self):
        bind(TransactionalSupport, to=self._old_transactional_support,
             scope=singleton)
        sess = self._tx_support.create_session()
        sess.rollback()
        sess.close()

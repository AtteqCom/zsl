"""
:mod:`zsl.service.service`
--------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>,
                  Peter Morihladko <morihladko@atteq.com>
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import logging
from functools import wraps

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session
from zsl.application.modules.alchemy_module import SessionHolder

from zsl import inject, Zsl


class SessionFactory(object):
    """Creates a db session with an open transaction."""

    @inject(session_holder=SessionHolder)
    def __init__(self, session_holder):
        self._session_holder = session_holder

    def create_session(self):
        # type: ()->Session
        return self._session_holder()


class TransactionHolder(object):
    def __init__(self):
        self._orm = None
        self._transaction_callback = []
        self._in_transaction = False

    def has_session(self):
        # type: () -> bool
        return self._orm is not None

    @property
    def session(self):
        # type: () -> Session
        return self._orm

    @property
    def in_transaction(self):
        return self._in_transaction

    def inject_session(self, session):
        # type: (Session) -> None
        """Used to set the session in the @transactional decorator."""
        self._orm = session
        self._in_transaction = True

    def commit(self):
        logging.getLogger(__name__).debug("Commit.")
        self._orm.commit()

    def rollback(self):
        logging.getLogger(__name__).debug("Rollback.")
        self._orm.rollback()

    def close(self):
        logging.getLogger(__name__).debug("Close.")
        self._orm.close()
        self._orm = None
        self._in_transaction = False

    def append_transaction_callback(self, callback):
        self._transaction_callback.append(callback)

    def run_transaction_callbacks(self):
        callbacks = self._transaction_callback
        self._transaction_callback = []
        for c in callbacks:
            c()


class EmptyTransactionalHolder(object):
    def __init__(self):
        self._session = None

    @property
    def session(self):
        return self._session


_EMPTY_TX_HOLDER = EmptyTransactionalHolder()


class TransactionalSupportMixin(object):
    """This mixin allows the objects to access transactional holder."""

    @property
    def _orm(self):
        # type: ()->Session
        return getattr(self, _TX_HOLDER_ATTRIBUTE, _EMPTY_TX_HOLDER).session


class Service(TransactionalSupportMixin):
    """
    Main service class.
    """

    @inject(app=Zsl, engine=Engine)
    def __init__(self, app, engine):
        """Constructor - initializes and injects the needed libraries."""
        super(Service, self).__init__()
        self._app = app
        self._engine = engine


_TX_HOLDER_ATTRIBUTE = '_tx_holder'


def transactional(f):
    @inject(session_factory=SessionFactory)
    def _get_session_factory(session_factory):
        # type: (SessionFactory) -> SessionFactory
        return session_factory

    @wraps(f)
    def transactional_f(service, *args, **kwargs):
        session_factory = _get_session_factory()
        trans_close = False

        if hasattr(service, _TX_HOLDER_ATTRIBUTE):
            tx_holder = getattr(service, _TX_HOLDER_ATTRIBUTE)
            assert tx_holder.has_session()
        else:
            tx_holder = TransactionHolder()
            setattr(service, _TX_HOLDER_ATTRIBUTE, tx_holder)
            trans_close = True

        try:
            logging.getLogger(__name__).debug("Entering transactional "
                                              "method.")
            if not tx_holder.has_session():
                session = session_factory.create_session()
                tx_holder.inject_session(session)

            rv = f(service, *args, **kwargs)

            if trans_close:
                tx_holder.run_transaction_callbacks()
                tx_holder.commit()

            return rv
        except:
            if trans_close:
                tx_holder.rollback()
            raise
        finally:
            if trans_close:
                tx_holder.close()
                delattr(service, _TX_HOLDER_ATTRIBUTE)

    return transactional_f

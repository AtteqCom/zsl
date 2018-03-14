"""
:mod:`zsl.service.service`
--------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>,
                  Peter Morihladko <morihladko@atteq.com>
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *  # NOQA
from functools import wraps
import logging

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session

from zsl import Zsl, inject
from zsl.application.modules.alchemy_module import EmptyTransactionalHolder, SessionFactory, TransactionHolderFactory

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

    @inject(tx_holder_factory=TransactionHolderFactory)
    def _get_tx_holder_factory(tx_holder_factory):
        # type: (TransactionHolderFactory) -> TransactionHolderFactory
        return tx_holder_factory

    @wraps(f)
    def transactional_f(service, *args, **kwargs):
        session_factory = _get_session_factory()
        trans_close = False

        if hasattr(service, _TX_HOLDER_ATTRIBUTE):
            tx_holder = getattr(service, _TX_HOLDER_ATTRIBUTE)
            assert tx_holder.has_session()
        else:
            tx_holder = _get_tx_holder_factory().create_transaction_holder()
            setattr(service, _TX_HOLDER_ATTRIBUTE, tx_holder)
            trans_close = True

        try:
            logging.getLogger(__name__).debug("Entering transactional "
                                              "method.")
            if not tx_holder.has_session():
                session = session_factory.create_session()
                tx_holder.inject_session(session)

            tx_holder.begin()

            rv = f(service, *args, **kwargs)

            if trans_close:
                tx_holder.run_transaction_callbacks()
                tx_holder.commit()

            return rv
        except:  # NOQA
            if trans_close:
                tx_holder.rollback()
            raise
        finally:
            logging.getLogger(__name__).debug("Finishing transactional "
                                              "method.")
            if trans_close:
                tx_holder.close()
                delattr(service, _TX_HOLDER_ATTRIBUTE)
                logging.getLogger(__name__).debug("Closing TX session.")

    return transactional_f

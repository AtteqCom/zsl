"""
:mod:`zsl.service.service`
--------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals
from builtins import object

import logging
from functools import wraps

from sqlalchemy.engine.base import Engine
from zsl.application.modules.alchemy_module import SessionHolder

from zsl import inject, Zsl, Injected


class TransactionalSupport(object):
    @inject(session_holder=SessionHolder)
    def __init__(self, session_holder):
        self._orm = None
        self._session_holder = session_holder
        self._in_transaction = False
        self._transaction_callback = []

    def append_transaction_callback(self, callback):
        self._transaction_callback.append(callback)


class Service(TransactionalSupport):
    """
    Main service class.
    """

    @inject(app=Zsl, engine=Engine)
    def __init__(self, app, engine):
        """
        Constructor - initializes and injects the needed libraries.
        """
        super(Service, self).__init__()
        self._app = app
        self._engine = engine


def transactional(f):
    @wraps(f)
    def transactional_f(*args, **kwargs):
        trans_close = False

        service_instance = args[0]

        try:
            logging.debug("Entering transactional method.")
            if service_instance._orm is None:
                service_instance._orm = service_instance._session_holder()

            if not service_instance._in_transaction:
                trans_close = True
                service_instance._in_transaction = True
                logging.debug("Transaction opened.")

            rv = f(*args, **kwargs)

            if trans_close:
                if service_instance._transaction_callback is not None:
                    callbacks = service_instance._transaction_callback
                    service_instance._transaction_callback = []
                    for c in callbacks:
                        c()

                logging.debug("Commit.")
                service_instance._orm.commit()

            return rv
        except:
            logging.debug("Rollback.")
            if trans_close and service_instance._orm is not None:
                service_instance._orm.rollback()
            raise
        finally:
            if trans_close:
                service_instance._orm.close()
                service_instance._in_transaction = False

    return transactional_f

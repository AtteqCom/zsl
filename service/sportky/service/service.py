'''
Created on 24.1.2013

@author: Martin Babka
'''

from application.service_application import SportkyFlask, service_application
from injector import inject
from sqlalchemy.engine.base import Engine
from application.initializers.database_initializer import SessionHolder

class Service(object):
    '''
    Main service class.
    '''

    @inject(session_holder=SessionHolder, app=SportkyFlask, engine=Engine)
    def __init__(self, session_holder, app, engine):
        '''
        Constructor - initializes and injects the needed libraries.
        '''
        self._orm = None
        self._session_holder = session_holder
        self._app = app
        self._engine = engine
        self._in_transaction = False
        self._transaction_callback = []

    def append_transaction_callback(self, callback):
        self._transaction_callback.append(callback)

def transactional(f):
    def transactional_f(*a):
        trans_close = False
        try:
            service_application.logger.debug("Entering transactional method.")
            if a[0]._orm == None:
                a[0]._orm = a[0]._session_holder()

            if not a[0]._in_transaction:
                trans_close = True
                service_application.logger.debug("Transaction opened.")

            rv = f(*a)
            if a[0]._transaction_callback != None:
                callbacks = a[0]._transaction_callback
                a[0]._transaction_callback = []
                for c in callbacks:
                    c()

            if trans_close:
                service_application.logger.debug("Commit.")
                a[0]._orm.commit()

            return rv
        except:
            service_application.logger.debug("Rollback.")
            if trans_close and a[0]._orm != None:
                a[0]._orm.rollback()
            raise
        finally:
            if trans_close:
                a[0]._in_transaction = False

    return transactional_f

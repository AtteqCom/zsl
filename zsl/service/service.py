'''
:mod:`asl.service.service`

.. moduleauthor:: Martin Babka
'''

from zsl.application.service_application import AtteqServiceFlask, service_application
from zsl.utils.injection_helper import inject
from sqlalchemy.engine.base import Engine
from zsl.application.initializers.database_initializer import SessionHolder
from functools import wraps

class SqlSesionMixin(object):
    """
    Prida podporu pre ``transactional`` dekorator pre metody triedy, 
    ktora implementuje tento mixin. Samotna session potom bude dostupna
    cez premennu ``self._orm`` v metode, na ktorej je zaveseny
    ``transactional`` dekorator
    
    Zatial treba inicializovat metodou ``init_sql_session``. 
    """
    
    @inject(session_holder=SessionHolder)
    def init_sql_session(self, session_holder):
        self._orm = None
        self._session_holder = session_holder
        self._in_transaction = False
        self._transaction_callback = []
    
    def append_transaction_callback(self, callback):
        self._transaction_callback.append(callback)
        
class TransactionalSupport(object):
    
    @inject(session_holder=SessionHolder)
    def __init__(self, session_holder):
        self._orm = None
        self._session_holder = session_holder
        self._in_transaction = False
        self._transaction_callback = []
        

class Service(TransactionalSupport):
    '''
    Main service class.
    '''

    @inject(app=AtteqServiceFlask, engine=Engine)
    def __init__(self, app, engine):
        '''
        Constructor - initializes and injects the needed libraries.
        '''
        super(Service, self).__init__()
        self._app = app
        self._engine = engine

    def append_transaction_callback(self, callback):
        self._transaction_callback.append(callback)

def transactional(f):

    @wraps(f)
    def transactional_f(*args, **kwargs):
        trans_close = False

        service_instance = args[0]

        try:
            service_application.logger.debug("Entering transactional method.")
            if service_instance._orm == None:
                service_instance._orm = service_instance._session_holder()

            if not service_instance._in_transaction:
                trans_close = True
                service_instance._in_transaction = True
                service_application.logger.debug("Transaction opened.")

            rv = f(*args, **kwargs)

            if trans_close:
                if service_instance._transaction_callback != None:
                    callbacks = service_instance._transaction_callback
                    service_instance._transaction_callback = []
                    for c in callbacks:
                        c()

                service_application.logger.debug("Commit.")
                service_instance._orm.commit()

            return rv
        except:
            service_application.logger.debug("Rollback.")
            if trans_close and service_instance._orm != None:
                service_instance._orm.rollback()
            raise
        finally:
            if trans_close:
                service_instance._orm.close()
                service_instance._in_transaction = False

    return transactional_f

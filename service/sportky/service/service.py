'''
Created on 24.1.2013

@author: Martin Babka
'''

import sqlalchemy
from application.service_application import SportkyFlask
from injector import inject

class Service(object):
    '''
    Main service class.
    '''

    @inject(session=sqlalchemy.orm.Session, app=SportkyFlask)
    def __init__(self, session, app):
        '''
        Constructor - initializes and injects the needed libraries.
        '''
        self._orm = session
        self._app = app

def transactional(f):
    def transactional_f(*a):
        try:
            return f(*a)
            a[0]._orm.commit()
        except Exception as e:
            a[0]._orm.rollback()
            raise e
    return transactional_f

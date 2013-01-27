'''
Created on 24.1.2013

@author: Martin Babka
'''
from sportky.service.service import Service, transactional
from db.models.raw import State

class StateService(Service):
    '''
    Service handling the states table.
    '''

    def __init__(self):
        Service.__init__(self)

    @transactional
    def fetch_list(self):
        return self._orm.query(State).all()

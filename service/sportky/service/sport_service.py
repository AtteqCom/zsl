'''
Created on 24.1.2013

@author: Martin Babka
'''
from sportky.service.service import Service, transactional
from db.models.raw import Sport

class SportService(Service):
    '''
    Service handling the sports table.
    '''

    def __init__(self):
        Service.__init__(self)

    @transactional
    def fetch_list(self):
        return self._orm.query(Sport).all()

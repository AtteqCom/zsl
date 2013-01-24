'''
Created on 24.1.2013

@author: Martin Babka
'''
from sportky.service.service import Service, transactional

class ClubService(Service):

    '''
    Service handling the clubs.
    '''
    def __init__(self):
        Service.__init__(self)

    @transactional
    def save(self, club):
        if (club.id == None):
            self._orm.add(club)
            self._orm.commit()

        club.update_url()

    def fetch(self, id):
        pass

    def delete(self, id):
        pass

    def fetch_list(self, filter, pagination, sorter):
        pass

    def fetch_random_club_ids(self, count):
        pass

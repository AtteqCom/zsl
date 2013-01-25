'''
Created on 24.1.2013

@author: Martin Babka
'''
from sportky.service.service import Service, transactional
from db.models.raw import SportClub, SportClubField, State, Sport

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

    @transactional
    def fetch(self, id):
        return self._orm.query(SportClub).outerjoin(SportClubField).outerjoin(State).outerjoin(Sport).filter(SportClub.id == id).one()

    @transactional
    def delete(self, id):
        self._orm.query(SportClub).filter(SportClub.id == id).delete()

    def fetch_list(self, filter, pagination, sorter):
        pass

    def fetch_random_club_ids(self, count):
        pass

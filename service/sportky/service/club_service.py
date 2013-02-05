'''
Created on 24.1.2013

@author: Martin Babka
'''
from sportky.service.service import Service, transactional
from db.models.raw import SportClub, SportClubField, State, Sport, Image
from db.helpers.query_helper import QueryHelper
import random
from sqlalchemy.sql.expression import asc

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

        for f in club.sport_club_fields:
            self._app.logger.debug("Adding field {0}.".format(f.name))
            self._orm.add(f)

        club.update_url()

    @transactional
    def fetch(self, id):
        return self._orm.query(SportClub).outerjoin(SportClubField).outerjoin(Image).outerjoin(State).outerjoin(Sport).filter(SportClub.id == id).one()

    @transactional
    def delete_sport_club_by_id(self, id):
        self._orm.query(SportClub).filter(SportClub.id == id).delete()

    @transactional
    def deactivate_sport_club_by_id(self, id):
        club = self._orm.query(SportClub).filter(SportClub.id == id).one()
        club.active = False
        self.save(club)

    @transactional
    def activate_sport_club_by_id(self, id):
        club = self._orm.query(SportClub).filter(SportClub.id == id).one()
        club.active = True
        self.save(club)

    @transactional
    def delete_sport_club_field(self, f):
        self._orm.delete(f)

    @transactional
    def fetch_list(self, filter, pagination, sorter):
        qh = QueryHelper(SportClub, filter, pagination, sorter)
        return (qh.execute(self._orm.query(SportClub).outerjoin(SportClub.sport).outerjoin(SportClub.state)), qh)

    @transactional
    def fetch_random_club_ids(self, count, only_toppped, only_active):
        q = self._orm.query(SportClub)
        if only_toppped:
            self._app.logger.info("Fetching only topped clubs.")
            q = q.filter(SportClub.top == 1)
        if only_active:
            self._app.logger.info("Fetching only active clubs.")
            q = q.filter(SportClub.active == 1)

        club_count = q.count()
        self._app.logger.info("Relevant club count {0}.".format(club_count))
        ids = []

        for i in random.sample(xrange(club_count), min(count, club_count)):
            q = self._orm.query(SportClub)

            if only_toppped:
                q = q.filter(SportClub.top == 1)
            if only_active:
                q = q.filter(SportClub.active == 1)

            club = q.order_by(asc(SportClub.id)).limit(1).offset(i).one()
            ids.append(club.id)

        return ids


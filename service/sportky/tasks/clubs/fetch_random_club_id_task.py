from task.task_decorator import json_input, json_output
from injector import inject
import sqlalchemy.orm
from db.models.raw import SportClub
import logging
import random
from sqlalchemy.sql.expression import asc

class FetchRandomClubIdTask(object):

    @inject(session=sqlalchemy.orm.Session, logger=logging.Logger)
    def __init__(self, session, logger):
        self.__orm = session
        self.__logger = logger

    @json_input
    @json_output
    def perform(self, data):
        d = data.get_data()
        club_count = self.__orm.query(SportClub).count()

        ids = []
        for i in random.sample(xrange(club_count), min(d['count'], club_count)):
            club = self.__orm.query(SportClub).order_by(asc(SportClub.id)).limit(1).offset(i).one()
            ids.append(club.id)
        return ids

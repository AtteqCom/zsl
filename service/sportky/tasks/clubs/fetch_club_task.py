from task.task_decorator import json_input, json_output
from injector import inject
import sqlalchemy.orm
from db.models.raw import SportClub, SportClubField, Sport, State
import logging

class FetchClubTask(object):

    @inject(session=sqlalchemy.orm.Session, logger=logging.Logger)
    def __init__(self, session, logger):
        self.__orm = session
        self.__logger = logger

    @json_input
    @json_output
    def perform(self, data):
        club = self.__orm.query(SportClub).outerjoin(SportClubField).outerjoin(State).outerjoin(Sport).filter(SportClub.id == data.get_data()['id']).one()
        return club.get_app_model()

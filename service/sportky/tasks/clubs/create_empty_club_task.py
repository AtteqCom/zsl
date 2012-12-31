from task.task_decorator import json_input, json_output
from injector import inject
import sqlalchemy.orm
from db.models.raw import SportClub
import logging
from datetime import datetime

class CreateEmptyClubTask(object):

    @inject(session=sqlalchemy.orm.Session, logger=logging.Logger)
    def __init__(self, session, logger):
        self.__orm = session
        self.__logger = logger

    @json_input
    @json_output
    def perform(self, data):
        c = SportClub()
        c.added = datetime.now()
        c.active = False
        c.flag_created_year = False
        c.city = ''
        c.coach = ''
        c.current_squad = False
        c.homepage = ''
        c.league = ''
        c.name = ''
        c.president = ''
        c.stadium = ''
        c.magazine_id = data.get_data()['magazine_id']
        c.url = ''
        self.__orm.add(c)
        self.__orm.commit()

        c.update_url()
        self.__orm.commit()

        return { 'id': c.id }

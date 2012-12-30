from task.task_decorator import json_input, json_output
from injector import inject
import sqlalchemy.orm
from db.models.raw import SportClub
import logging

class DeleteTask(object):

    @inject(Session=sqlalchemy.orm.Session, logger=logging.Logger)
    def __init__(self, Session, logger):
        self.__orm = Session
        self.__logger = logger

    @json_input
    @json_output
    def perform(self, data):
        try:
            self.__orm.query(SportClub).filter(SportClub.id == data.get_data()['id']).delete()
            res = True
        except Exception as e:
            res = False
            self.__logger.error(e)

        return {'result': res}

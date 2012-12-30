from injector import inject
import sqlalchemy.orm

from application.service_application import service_application
from task.task_decorator import json_output
app = service_application
from db.models.raw import Sport

class FetchSportListTask(object):

    @inject(Session=sqlalchemy.orm.Session)
    def __init__(self, Session):
        self.__orm = Session

    @json_output
    def perform(self, data):
        sports = []
        for s in self.__orm.query(Sport).all():
            sports.append(s.get_app_model())

        return sports

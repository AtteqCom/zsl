from injector import inject
import sqlalchemy.orm

from application.service_application import service_application
from task.task_decorator import json_output
app = service_application
from db.models.raw import State

class FetchStateListTask(object):

    @inject(Session=sqlalchemy.orm.Session)
    def __init__(self, Session):
        self.__orm = Session

    @json_output
    def perform(self, data):
        states = []
        for s in self.__orm.query(State).all():
            states.append(s.get_app_model())

        return states

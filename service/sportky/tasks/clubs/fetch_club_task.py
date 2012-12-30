from task.task_decorator import json_input, json_output
from injector import inject
import sqlalchemy.orm

from application.service_application import service_application
app = service_application

class FetchClubTask(object):

    @inject(Session=sqlalchemy.orm.Session)
    def __init__(self, Session):
        self.__orm = Session

    @json_input
    @json_output
    def perform(self, data):
        app.logger.debug("Fetch clubs called.")
        app.logger.debug("Data {0}.".format(data.get_data()))

        sess = self.__orm()
        sess.query()

        return { 'clubs': [ { 'id': '1', 'name': 'FBC Emphatic', 'state': 'CR', 'sport': 'Floorball' } ], 'count': 1 }

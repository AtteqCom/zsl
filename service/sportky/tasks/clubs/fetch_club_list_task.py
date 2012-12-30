from task.task_decorator import json_input, json_output
from injector import inject
import sqlalchemy.orm

from application.service_application import service_application
app = service_application
from db.models.raw import SportClub

class FetchClubListTask(object):

    @inject(Session=sqlalchemy.orm.Session)
    def __init__(self, Session):
        self.__orm = Session

    @json_input
    @json_output
    def perform(self, data):
        app.logger.debug("Fetch clubs called with data {0}.".format(data.get_data()))

        sess = self.__orm
        count = sess.query(SportClub).count()
        clubs = []
        for c in sess.query(SportClub).all():
            clubs.append(c.get_app_model())

        return { 'clubs': clubs, 'count': count }

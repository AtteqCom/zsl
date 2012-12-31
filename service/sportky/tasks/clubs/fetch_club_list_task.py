from task.task_decorator import json_input, json_output
from injector import inject
import sqlalchemy.orm

from application.service_application import service_application
from db.helpers.query_helper import QueryHelper
from db.helpers.query_filter import FILTER_VALUES,\
    FILTER_HINT, OperatorEq, OperatorLike
app = service_application
from db.models.raw import SportClub

class FetchClubListTask(object):

    @inject(session=sqlalchemy.orm.Session)
    def __init__(self, session):
        self.__orm = session

    @json_input
    @json_output
    def perform(self, data):
        d = data.get_data()
        app.logger.debug("Fetch clubs called with data {0}.".format(d))

        f = {
            FILTER_VALUES: d['filter'],
            FILTER_HINT: {
                 'sport_id': OperatorEq,
                 'state_id': OperatorEq,
                 'magazine_id': OperatorEq,
                 'name': OperatorLike
            }
        }
        qh = QueryHelper(SportClub, f, d['pagination'], d['sorter'])

        clubs = []
        for c in qh.execute(self.__orm.query(SportClub).join(SportClub.sport).join(SportClub.state)):
            club = c.get_app_model()
            club.sport = c.sport.name
            club.state = c.state.name_sk
            clubs.append(club)

        return { 'clubs': clubs, 'count': qh.get_pagination().get_record_count() }

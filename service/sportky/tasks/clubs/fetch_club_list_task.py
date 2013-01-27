from task.task_decorator import json_input, json_output
from injector import inject

from application.service_application import SportkyFlask
from db.helpers.query_filter import FILTER_VALUES,\
    FILTER_HINT, OperatorEq, OperatorLike
from sportky.service.club_service import ClubService

class FetchClubListTask(object):

    @inject(club_service=ClubService, app=SportkyFlask)
    def __init__(self, club_service, app):
        self._app = app
        self._club_service = club_service

    @json_input
    @json_output
    def perform(self, data):
        d = data.get_data()
        self._app.logger.debug("Fetch clubs called with data {0}.".format(d))

        f = {
            FILTER_VALUES: d['filter'],
            FILTER_HINT: {
                 'sport_id': OperatorEq,
                 'state_id': OperatorEq,
                 'magazine_id': OperatorEq,
                 'name': OperatorLike
            }
        }

        clubs = []
        (raw_clubs, qh) = self._club_service.fetch_list(f, d['pagination'], d['sorter'])
        for c in raw_clubs:
            club = c.get_app_model()
            if c.sport != None:
                club.sport = c.sport.name
            else:
                club.sport = None

            if c.state != None:
                club.state = c.state.name_sk
            else:
                club.state = None
            clubs.append(club)

        return { 'clubs': clubs, 'count': qh.get_pagination().get_record_count() }

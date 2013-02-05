from task.task_decorator import json_input, json_output
from injector import inject
from application.service_application import SportkyFlask
from sportky.service.club_service import ClubService

class FetchRandomClubIdTask(object):

    @inject(club_service=ClubService, app=SportkyFlask)
    def __init__(self, club_service, app):
        self._app = app
        self._club_service = club_service

    @json_input
    @json_output
    def perform(self, data):
        d = data.get_data()

        if not ('only_topped' in d):
            d['only_topped'] = True

        if not ('only_active' in d):
            d['only_active'] = True

        return self._club_service.fetch_random_club_ids(d['count'], d['only_topped'], d['only_active'])

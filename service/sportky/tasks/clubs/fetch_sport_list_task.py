from injector import inject
from task.task_decorator import json_output
from sportky.service.sport_service import SportService

class FetchSportListTask(object):

    @inject(sport_service=SportService)
    def __init__(self, sport_service):
        self._sport_service = sport_service

    @json_output
    def perform(self, data):
        sports = []
        for s in self._sport_service.fetch_list():
            sports.append(s.get_app_model())

        return sports

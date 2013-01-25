from task.task_decorator import json_input, json_output
from injector import inject
from application.service_application import SportkyFlask
from sportky.service.club_service import ClubService

class DeleteClubTask(object):

    @inject(club_service=ClubService, app=SportkyFlask)
    def __init__(self, club_service, app):
        self._club_service = club_service
        self._app = app

    @json_input
    @json_output
    def perform(self, data):
        try:
            self._club_service.delete(data.get_data()['id'])
            res = True
        except Exception as e:
            res = False
            self.__logger.error(e)

        return {'result': res}

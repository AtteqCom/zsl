from task.task_decorator import json_input, json_output
from injector import inject
from application.service_application import SportkyFlask
from sportky.service.club_service import ClubService

class FetchClubTask(object):

    @inject(club_service=ClubService, app=SportkyFlask)
    def __init__(self, club_service, app):
        self._club_service = club_service
        self._app = app

    @json_input
    @json_output
    def perform(self, data):
        rm = self._club_service.fetch(data.get_data()['id'])
        m = rm.get_app_model()
        if rm.image != None:
            self._app.logger.info("Having the image.")
            m.image.url = rm.image.get_url(135) # TODO: Nicely.
        else:
            self._app.logger.info("Not having the image.")
        return m

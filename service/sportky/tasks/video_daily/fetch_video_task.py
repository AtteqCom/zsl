from task.task_decorator import json_input, json_output
from injector import inject
from db.models.raw import VideoDaily
from datetime import datetime
from sportky.service.video_daily_service import VideoDailyService
from application.service_application import SportkyFlask

class FetchVideoTask(object):

    @inject(video_daily_service = VideoDailyService, app = SportkyFlask)
    def __init__(self, video_daily_service, app):
        self._app = app
        self._video_daily_service = video_daily_service

    @json_input
    @json_output
    def perform(self, data):
        d = data.get_data()
        v = self._video_daily_service.fetch(d['vdid'])

        #self._app.logger.debug("App video id " + format(type(videos[0].vdid)))
        #self._app.logger.debug("App video created " + format(type(videos[0].created)))

        return v.get_app_model()

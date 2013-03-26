from task.task_decorator import json_input, json_output
from injector import inject
from db.models.raw import VideoDaily
from datetime import datetime
from sportky.service.video_daily_service import VideoDailyService
from application.service_application import SportkyFlask

class CreateEmptyVideoDailyTask(object):

    @inject(video_daily_service = VideoDailyService, app = SportkyFlask)
    def __init__(self, video_daily_service, app):
        self._app = app
        self._video_daily_service = video_daily_service

    @json_input
    @json_output
    def perform(self, data):
        d = data.get_data()
        
        v = VideoDaily()
        v.created = datetime.now()
        v.description = ''
        v.embedded_code = ''
        v.name = ''
        v.date = ''
        v.magazine_id = d['magazine_id']

        self._video_daily_service.save(v)
        return { 'vdid': v.vdid }

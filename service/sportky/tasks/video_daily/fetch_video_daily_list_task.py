from task.task_decorator import json_input, json_output
from injector import inject
from db.models.raw import VideoDaily
from datetime import datetime
from sportky.service.video_daily_service import VideoDailyService
from application.service_application import SportkyFlask
from db.helpers.query_filter import FILTER_VALUES, FILTER_HINT, OperatorEq, OperatorLike
from db.helpers.sorter import Sorter
from db.helpers import app_models

class FetchVideoDailyListTask(object):

    @inject(video_daily_service = VideoDailyService, app = SportkyFlask)
    def __init__(self, video_daily_service, app):
        self._app = app
        self._video_daily_service = video_daily_service

    @json_input
    @json_output
    def perform(self, data):
        d = data.get_data()
        self._app.logger.debug("Fetch daily videos called with data {0}.".format(d))

        f = {
            FILTER_VALUES: d['filter'],
            FILTER_HINT: {
                 'magazine_id': OperatorEq,
                 'name': OperatorLike,
            }
        }

        (videos, qh) = self._video_daily_service.fetch_list(f,d['pagination'],Sorter(d['sorter']))

        return { 'videos': app_models(videos) }
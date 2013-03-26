from task.task_decorator import json_input, json_output
from injector import inject
from db.models.raw import VideoDaily
from db.models.raw.model_helper import ModelHelper
from datetime import date,datetime
from sportky.service.video_daily_service import VideoDailyService
from application.service_application import SportkyFlask
from db.models.validators import VideoDailyForm
from werkzeug.datastructures import MultiDict

class UpdateVideoDailyTask(object):

    @inject(video_daily_service = VideoDailyService, app = SportkyFlask)
    def __init__(self, video_daily_service, app):
        self._app = app
        self._video_daily_service = video_daily_service

    @json_input
    @json_output
    def perform(self, data):
        try:
            self._app.logger.debug("Updating video daily.")
            video_daily_data = data.get_data()['video_daily']

            f = VideoDailyForm(MultiDict(video_daily_data))
            self._app.logger.info("VideoDaily: {0}.".format(video_daily_data))
            if not f.validate():
                self._app.logger.info("Validation failed.");
                return {"result": False, "errors": f.errors}

            # konvertovanie stringu date do objektu date
            try:
                dt = datetime.strptime(video_daily_data['date'],'%d. %m. %Y')
                d = date(dt.year,dt.month,dt.day)
                video_daily_data['date'] = d
            except Exception:
                pass

            video_daily_db = self._video_daily_service.fetch(video_daily_data['vdid'])
            ModelHelper.update_model(video_daily_db,video_daily_data)

            self._video_daily_service.save(video_daily_db)
            res = True

        except Exception as e:
            self._app.logger.error(e)
            res = False

        return { 'result': res }

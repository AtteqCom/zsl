from asl.application.service_application import AtteqServiceFlask
from asl.utils.injection_helper import inject
from asl.utils.gearman_helper import schedule_gearman_task


class ScheduleGearmanTask(object):

    @inject(app=AtteqServiceFlask)
    def __init__(self, app):
        self._app = app

    def perform(self, data):
        data = data.get_data()

        # Create gearman.
        schedule_gearman_task(self._app, data['path'], data['data'])

        return 'job submitted'

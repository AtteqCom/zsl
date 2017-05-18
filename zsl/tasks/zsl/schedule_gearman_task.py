"""
:mod:`zsl.tasks.asl.schedule_gearman_task`
------------------------------------------
"""
from __future__ import unicode_literals
from builtins import object
from zsl import Zsl
from zsl import inject
from zsl.utils.gearman_helper import schedule_gearman_task


class ScheduleGearmanTask(object):

    @inject(app=Zsl)
    def __init__(self, app):
        self._app = app

    def perform(self, data):
        data = data.get_data()

        # Create gearman.
        schedule_gearman_task(self._app, data['path'], data['data'])

        return 'job submitted'

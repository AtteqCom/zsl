"""
:mod:`zsl.tasks.asl.schedule_kill_worker_task`
----------------------------------------------
"""
from __future__ import unicode_literals
from builtins import object
from zsl.application.service_application import AtteqServiceFlask
from zsl.utils.injection_helper import inject
from zsl.utils.gearman_helper import schedule_gearman_task


class ScheduleKillWorkerTask(object):

    @inject(app=AtteqServiceFlask)
    def __init__(self, app):
        self._app = app

    def perform(self, data):
        data = data.get_data()

        # Create gearman.
        schedule_gearman_task(self._app, 'zsl/kill_worker_task', {})

        return 'job submitted'

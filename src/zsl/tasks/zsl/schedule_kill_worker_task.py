"""
:mod:`zsl.tasks.asl.schedule_kill_worker_task`
----------------------------------------------
"""
from __future__ import unicode_literals

from builtins import object

from zsl.utils.gearman_helper import schedule_gearman_task


class ScheduleKillWorkerTask(object):
    def perform(self, _):
        # Create gearman.
        schedule_gearman_task('zsl/kill_worker_task', {})
        return 'job submitted'

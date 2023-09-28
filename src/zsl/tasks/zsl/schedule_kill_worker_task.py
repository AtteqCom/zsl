"""
:mod:`zsl.tasks.asl.schedule_kill_worker_task`
----------------------------------------------
"""
from zsl.utils.gearman_helper import schedule_gearman_task


class ScheduleKillWorkerTask:
    def perform(self, _):
        # Create gearman.
        schedule_gearman_task('zsl/kill_worker_task', {})
        return 'job submitted'

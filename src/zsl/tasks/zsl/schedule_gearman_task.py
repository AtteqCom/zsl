"""
:mod:`zsl.tasks.asl.schedule_gearman_task`
------------------------------------------
"""
from zsl.task.task_data import TaskData
from zsl.utils.gearman_helper import schedule_gearman_task


class ScheduleGearmanTask:

    def perform(self, data):
        # type: (TaskData)->str
        data = data.payload

        # Create gearman.
        schedule_gearman_task(data['path'], data['data'])

        return 'job submitted'

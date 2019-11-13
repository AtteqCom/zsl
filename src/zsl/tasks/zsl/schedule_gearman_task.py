"""
:mod:`zsl.tasks.asl.schedule_gearman_task`
------------------------------------------
"""
from __future__ import unicode_literals

from builtins import object

from zsl.task.task_data import TaskData
from zsl.utils.gearman_helper import schedule_gearman_task


class ScheduleGearmanTask(object):

    def perform(self, data):
        # type: (TaskData)->str
        data = data.payload

        # Create gearman.
        schedule_gearman_task(data['path'], data['data'])

        return 'job submitted'

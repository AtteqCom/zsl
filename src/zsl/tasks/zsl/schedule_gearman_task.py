"""
:mod:`zsl.tasks.asl.schedule_gearman_task`
------------------------------------------
"""
from __future__ import unicode_literals

from builtins import object

from zsl.utils.gearman_helper import schedule_gearman_task


class ScheduleGearmanTask(object):

    def perform(self, data):
        data = data.get_data()

        # Create gearman.
        schedule_gearman_task(data['path'], data['data'])

        return 'job submitted'

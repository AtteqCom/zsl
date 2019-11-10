"""
:mod:`zsl.tasks.asl.schedule_gearman_task`
------------------------------------------
"""
from __future__ import unicode_literals

from builtins import object

from zsl.interface.celery.worker import create_celery_app, zsl_task
from zsl.task.task_data import TaskData
from zsl.task.task_decorator import json_input


def schedule_celery_task(path, data):
    # type: (str, TaskData)->None
    zsl_task.delay({"path": path, "data": data})


class ScheduleCeleryTask(object):
    @json_input
    def perform(self, data):
        # type: (TaskData)->str
        data = data.payload
        schedule_celery_task(data["path"], data["data"])
        return "job submitted"

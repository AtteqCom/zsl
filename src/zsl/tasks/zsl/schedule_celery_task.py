"""
:mod:`zsl.tasks.asl.schedule_gearman_task`
------------------------------------------
"""
from __future__ import unicode_literals
from builtins import object

from zsl.task.task_decorator import json_input

from zsl.interface.celery.worker import zsl_task, create_celery_app


def schedule_celery_task(path, data):
    app = create_celery_app()
    zsl_task.delay({'path': path, 'data': data})


class ScheduleCeleryTask(object):
    @json_input
    def perform(self, data):
        data = data.get_data()
        schedule_celery_task(data['path'], data['data'])
        return 'job submitted'

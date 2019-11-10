"""
:mod:`zsl.tasks.asl.sum_task`
-----------------------------

Created on 22.12.2012

..moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

from builtins import object

from injector import inject

from zsl import Zsl
from zsl.task.task_data import TaskData
from zsl.task.task_decorator import json_input, json_output


class SumTask(object):
    @inject(app=Zsl)
    def __init__(self, app):
        self._app = app

    @json_input
    @json_output
    def perform(self, data):
        # type: (TaskData)->str
        payload = data.payload
        self._app.logger.debug("Sum task with data '{0}'.".format(payload))
        return {"input": payload, "result": sum(payload)}

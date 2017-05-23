"""
:mod:`zsl.tasks.asl.sum_task`
-----------------------------

Created on 22.12.2012

..moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

from builtins import object
from zsl.task.task_decorator import json_input, json_output
from zsl import Zsl
from injector import inject


class SumTask(object):
    @inject(app=Zsl)
    def __init__(self, app):
        self._app = app

    @json_input
    @json_output
    def perform(self, data):
        self._app.logger.debug("Sum task with data '{0}'.".format(data.get_data()))
        return {"input": data.get_data(), "result": sum(data.get_data())}

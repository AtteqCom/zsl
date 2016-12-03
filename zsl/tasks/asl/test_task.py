"""
Created on 22.12.2012

@author: Martin Babka <babka@atteq.com>
"""

from zsl.task.task_decorator import json_input, json_output
from zsl.application.service_application import AtteqServiceFlask
from injector import inject


class TestTask(object):

    @inject(app=AtteqServiceFlask)
    def __init__(self, app):
        self._app = app

    @json_input
    @json_output
    def perform(self, data):
        return "ok"

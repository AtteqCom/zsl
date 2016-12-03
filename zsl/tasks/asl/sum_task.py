'''
Created on 22.12.2012

@author: Martin Babka
'''

from zsl.task.task_decorator import json_input, json_output
from zsl.application.service_application import AtteqServiceFlask
from injector import inject

class SumTask(object):

    @inject(app=AtteqServiceFlask)
    def __init__(self, app):
        self._app = app

    @json_input
    @json_output
    def perform(self, data):
        self._app.logger.debug("Sum task with data '{0}'.".format(data.get_data()))
        return {"input": data.get_data(), "result": sum(data.get_data())}

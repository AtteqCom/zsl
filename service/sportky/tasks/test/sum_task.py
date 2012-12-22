'''
Created on 22.12.2012

@author: Martin Babka
'''

from application.service_application import service_application
from task.task_decorator import json_input, json_output

app = service_application

class SumTask:
    @json_input
    @json_output
    def perform(self, data):
        app.logger.debug("Sum task with data '{0}'.".format(data.get_data()))
        return {"input": data.get_data(), "result": sum(data.get_data())}

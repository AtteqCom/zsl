"""
Created on 22.12.2012

@author: Martin Babka <babka@atteq.com>
"""

from asl.task.task_decorator import json_input, json_output, crossdomain
from asl.application.service_application import AtteqServiceFlask
from injector import inject


class CorsTestTask(object):

    @inject(app=AtteqServiceFlask)
    def __init__(self, app):
        self._app = app

    @json_input
    @json_output
    @crossdomain("www.atteq.com", methods=["GET", "OPTIONS"])
    def perform(self, data):
        return "ok"

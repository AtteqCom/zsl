"""
:mod:`zsl.tasks.asl.cors_test_task`
-----------------------------------

Created on 22.12.2012

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals

from builtins import object
from zsl.task.task_decorator import json_input, json_output, crossdomain
from zsl.application.service_application import AtteqServiceFlask
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

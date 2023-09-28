"""
:mod:`zsl.tasks.asl.cors_test_task`
-----------------------------------

Created on 22.12.2012

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from injector import inject

from zsl import Zsl
from zsl.task.task_decorator import crossdomain, json_input, json_output


class CorsTestTask:

    @inject(app=Zsl)
    def __init__(self, app):
        self._app = app

    @json_input
    @json_output
    @crossdomain(methods=["GET", "OPTIONS"])
    def perform(self, data):
        return "ok"

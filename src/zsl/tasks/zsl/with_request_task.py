"""
:mod:`zsl.tasks.asl.version_task`
---------------------------------

Created on 18.02.2019

..moduleauthor:: Julius Flimmel
"""
from __future__ import unicode_literals

from builtins import object

from zsl import Zsl, inject
from zsl.interface.task import payload_into_model
from zsl.task.task_decorator import json_input, json_output


class WithRequestTask(object):

    class Request:
        def __init__(self):
            self.list_of_numbers = []  # type : List[int]

    """
    Returns received data if any or 'empty'
    """

    @inject(app=Zsl)
    def __init__(self, app):
        self._app = app

    @json_input
    @json_output
    @payload_into_model(Request)
    def perform(self, request):
        return request.list_of_numbers if request.list_of_numbers else "empty"

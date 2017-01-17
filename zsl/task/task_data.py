"""
:mod:`zsl.task.task_data`
-------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals
from builtins import object


class TaskData(object):

    def __init__(self, app, data):
        self._app = app
        self._data = data
        self._is_skipping_json = False

    def get_data(self):
        return self._data

    def get_service_application(self):
        return self._app

    def transform_data(self, f):
        self._data = f(self._data) if self._data is not None else {}

    def is_skipping_json(self):
        return self._is_skipping_json

    def set_skipping_json(self, value):
        self._is_skipping_json = value

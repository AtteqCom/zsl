'''
Created on 14.12.2012

.. moduleauthor:: Martin Babka
'''
class TaskData:
    def __init__(self, app, data):
        self._app = app
        self._data = data
        self._is_skipping_json = False

    def get_data(self):
        return self._data;

    def get_service_application(self):
        return self._app

    def transform_data(self, f):
        self._data = f(self._data) if self._data != None else {}

    def is_skipping_json(self):
        return self._is_skipping_json

    def set_skipping_json(self, value):
        self._is_skipping_json = value

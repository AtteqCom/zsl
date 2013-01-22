'''
Created on 14.12.2012

@author: Martin Babka
'''
class TaskData:
    def __init__(self, app, data):
        self.__app = app
        self.__data = data
        self.__is_skipping_json = False

    def get_data(self):
        return self.__data;

    def get_service_application(self):
        return self.__app

    def transform_data(self, f):
        self.__data = f(self.__data)

    def is_skipping_json(self):
        return self.__is_skipping_json

    def set_skipping_json(self, value):
        self.__is_skipping_json = value

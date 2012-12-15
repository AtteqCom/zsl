'''
Created on 14.12.2012

@author: Martin Babka
'''
class TaskData:
    def __init__(self, app, data):
        self.__app = app
        self.__data = data

    def get_data(self):
        return self.__data;

    def get_service_application(self):
        return self.__app

    def transform_data(self, f):
        self.__data = f(self.__data)

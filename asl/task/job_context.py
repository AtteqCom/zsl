'''
Created on 8.4.2013

@author: Martin Babka
'''
from asl.task.task_data import TaskData
from asl.application.service_application import service_application
from abc import abstractmethod

class Job:
    def __init__(self, data):
        self.data = data

class JobContext:
    '''
    Job Context
    '''
    def __init__(self, job, task, task_callable):
        '''
        Constructor
        '''
        self.job = Job(job.data)
        self.task = task
        self.task_callable = task_callable
        self.task_data = TaskData(service_application, self.job.data['data'])

    @classmethod
    def get_current_context(cls):
        return cls._current_context

    @classmethod
    def set_current_context(cls, context):
        cls._current_context = context

class Responder:
    @abstractmethod
    def respond(self):
        pass

class WebJobContext(JobContext):
    def __init__(self, path, data, task, task_callable, request):
        '''
        Constructor
        '''
        self.job = Job({'data': data, 'path': path})
        self.task = task
        self.task_callable = task_callable
        self.task_data = TaskData(service_application, data)
        self._request = request
        self._responders = []

    def get_web_request(self):
        return self._request

    def add_responder(self, r):
        self._responders.append(r)

    def notify_responders(self, response):
        for r in self._responders:
            r.respond(response)

'''
Created on 8.4.2013

@author: Martin Babka
'''
from asl.task.task_data import TaskData
from asl.application.service_application import service_application

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

class WebJobContext(JobContext):
    def __init__(self, path, data, task, task_callable):
        '''
        Constructor
        '''
        self.job = Job({'data': data, 'path': path})
        self.task = task
        self.task_callable = task_callable
        self.task_data = TaskData(service_application, data)

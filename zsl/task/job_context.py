"""
:mod:`zsl.task.job_context`

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals
from builtins import object
from zsl.task.task_data import TaskData
from zsl.application.service_application import service_application
from abc import abstractmethod


class Job(object):
    def __init__(self, data):
        self.data = data


class JobContext(object):
    """
    Job Context
    """
    def __init__(self, job, task, task_callable):
        """
        Constructor
        """
        self.job = Job(job.data)
        self.task = task
        self.task_callable = task_callable
        self.task_data = TaskData(service_application, self.job.data['data'])
        self._current_context = None

    @classmethod
    def get_current_context(cls):
        return cls._current_context

    @classmethod
    def set_current_context(cls, context):
        cls._current_context = context


class Responder(object):

    @abstractmethod
    def respond(self, r):
        pass


def web_task_redirect(location):
    return {'headers': {'Location': location}, 'status_code': 301}


class WebJobContext(JobContext):
    def __init__(self, path, data, task, task_callable, request):
        """
        Constructor
        """
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

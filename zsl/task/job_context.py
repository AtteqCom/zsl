"""
:mod:`zsl.task.job_context`
---------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals
from builtins import object
from typing import Callable
from abc import abstractmethod

from zsl.task.task_data import TaskData


class Job(object):
    def __init__(self, data):
        # type: (dict) -> None

        self.data = data

    @property
    def path(self):
        """Job's path.

        :getter: Returns job's path
        :type: str
        """
        return self.data['path']

    @property
    def payload(self):
        """Data part of job.

        :getter: Returns job's payload
        :type: dict
        """
        return self.data['data']

    @property
    def is_valid(self):
        """Validity of job's data.

        :getter: Returns if job's data are valid
        :type: bool
        """
        return self.data and 'path' in self.data and 'data' in self.data


class JobContext(object):
    """Job Context"""

    _current_context = None

    def __init__(self, job, task, task_callable):
        # type: (Job, object, Callable) -> None
        """
        Constructor
        """
        self.job = job
        self.task = task
        self.task_callable = task_callable
        self.task_data = TaskData(self.job.payload)

        JobContext.set_current_context(None)

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
        """Constructor"""

        self.job = Job({'data': data, 'path': path})
        self.task = task
        self.task_callable = task_callable
        self.task_data = TaskData(data)
        self._request = request
        self._responders = []

    def get_web_request(self):
        return self._request

    def add_responder(self, r):
        self._responders.append(r)

    def notify_responders(self, response):
        for r in self._responders:
            r.respond(response)

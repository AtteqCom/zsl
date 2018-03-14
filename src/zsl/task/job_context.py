"""
:mod:`zsl.task.job_context`
---------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from abc import abstractmethod
from builtins import *
import contextlib
from threading import current_thread
from typing import Callable, Dict

from flask.wrappers import Response

from zsl.task.task_data import TaskData
from zsl.utils.reflection_helper import proxy_object_to_delegate


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

    def __init__(self, job, task, task_callable):
        # type: (Job, object, Callable) -> None
        """
        Constructor
        """
        self._job = job
        self._task = task
        self._task_callable = task_callable
        self._task_data = TaskData(self.job.payload)

        JobContext._set_current_context(self)

    @property
    def job(self):
        return self._job

    @property
    def task(self):
        return self._task

    @property
    def task_callable(self):
        return self._task_callable

    @property
    def task_data(self):
        return self._task_data

    @classmethod
    def get_current_context(cls):
        return current_thread()._current_job_context

    @classmethod
    def _set_current_context(cls, context):
        current_thread()._current_job_context = context


class Responder(object):
    @abstractmethod
    def respond(self, r):
        pass


class StatusCodeResponder(Responder):
    def __init__(self, status_code):
        # type: (int)->None
        self._status_code = status_code

    def respond(self, r):
        # type: (Response)->None
        r.status_code = self._status_code


def add_responder(responder):
    # type:(Responder)->None
    jc = JobContext.get_current_context()
    if isinstance(jc, WebJobContext):
        jc.add_responder(responder)


def web_task_redirect(location):
    return {'headers': {'Location': location}, 'status_code': 301}


def create_job(path, data):
    # type: (str, Dict[str, Any])->Job
    return Job({'data': data, 'path': path})


class WebJobContext(JobContext):
    def __init__(self, path, data, task, task_callable, request):
        """Constructor"""
        super(WebJobContext, self).__init__(create_job(path, data), task, task_callable)
        self._request = request
        self._responders = []

    def get_web_request(self):
        return self._request

    def add_responder(self, r):
        self._responders.append(r)

    def notify_responders(self, response):
        try:
            for r in self._responders:
                r.respond(response)
        finally:
            self._responders = []


class DelegatingJobContext(JobContext):
    def __init__(self, job, task, task_callable):
        wrapped_job_context = JobContext.get_current_context()
        super(DelegatingJobContext, self).__init__(job, task, task_callable)
        self._wrapped_job_context = wrapped_job_context
        proxy_object_to_delegate(self, wrapped_job_context)

    def stop_delegating(self):
        JobContext._set_current_context(self._wrapped_job_context)


@contextlib.contextmanager
def delegating_job_context(job, task, task_callable):
    djc = DelegatingJobContext(job, task, task_callable)
    yield djc
    djc.stop_delegating()

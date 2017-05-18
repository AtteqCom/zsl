"""
:mod:`zsl.tasks.asl.kill_worker_task`
-------------------------------------

Created on 22.12.2012

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

from builtins import object
from zsl import Zsl
from injector import inject
from zsl.task.job_context import JobContext, WebJobContext
from zsl.interface.task_queue import KillWorkerException


class KillWorkerTask(object):
    @inject(app=Zsl)
    def __init__(self, app):
        self._app = app

    @staticmethod
    def perform(data):
        if isinstance(JobContext.get_current_context(), WebJobContext):
            raise Exception("Can not kill worker from web!")

        raise KillWorkerException()

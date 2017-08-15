"""
:mod:`zsl.interface.celery.worker`
----------------------------------

Implementation of celery workers.

.. moduleauthor:: Peter Morihladko
"""
from __future__ import unicode_literals

import sys

from celery import Celery, shared_task
from injector import Module, provides, singleton

from zsl import Config, inject
from zsl.interface.task_queue import TaskQueueWorker
from zsl.task.job_context import Job


class CeleryTaskQueueWorkerBase(TaskQueueWorker):
    """Base class for celery task queue worker.

    It contains only the task execution part of worker.
    """

    def execute_celery_task(self, job_data):
        # type: (dict) -> dict
        """Creates job from task and executes the job.

        :param job_data: job's data
        :return: job results
        :rtype: dict
        """
        job = Job(job_data)
        return self.execute_job(job)


class CeleryTaskQueueOutsideWorker(CeleryTaskQueueWorkerBase):
    """Celery worker used only for task execution.

    This can be used when the worker is manage with some other application,
    like `celery worker` or `celery multi`.
    """

    def stop_worker(self):
        self._app.logger.error("Running from celery worker, kill from shell!")

    def run(self):
        self._app.logger.error("Running from celery worker, start from shell!")


@inject(config=Config)
def create_celery_app(config):
    # type:(Config)->Celery
    celery_app = Celery()
    celery_app.config_from_object(config['CELERY'])
    return celery_app


class CeleryTaskQueueMainWorker(CeleryTaskQueueWorkerBase):
    """Worker implementation for Celery task queue."""

    def __init__(self, ):
        super(CeleryTaskQueueMainWorker, self).__init__()
        self.celery_app = create_celery_app()
        self.celery_worker = None

    def stop_worker(self):
        self._app.logger.info("Stopping Celery worker on demand - quitting.")
        self.celery_worker.stop()

    def run(self, argv, *args, **kwargs):
        self._app.logger.info("Running the worker.")
        self.celery_worker = self.celery_app.worker_main((sys.argv[0],) + argv)


@shared_task
@inject(worker=CeleryTaskQueueWorkerBase)
def zsl_task(job_data, worker):
    # type: (dict, CeleryTaskQueueWorkerBase) -> dict
    """This function will be registered as a celery task.

    :param job_data: task data
    :param worker: current celery worker
    :type worker: CeleryTaskQueueWorkerBase
    :return: task results
    """
    return worker.execute_celery_task(job_data)

from __future__ import unicode_literals

import sys

from celery import Celery, shared_task
from injector import Module, singleton, provides

from zsl import Config
from zsl.utils.injection_helper import inject
from zsl.interface.task_queue import TaskQueueWorker
from zsl.task.job_context import Job


class CeleryTaskQueueWorkerBase(TaskQueueWorker):

    @inject(config=Config)
    def __init__(self, config):
        # type: (Config) -> None
        super(CeleryTaskQueueWorkerBase, self).__init__()

        self.celery_app = Celery()
        self.celery_app.config_from_object(config['CELERY'])

    def execute_celery_task(self, job_data):
        job = Job(job_data)

        return self.execute_job(job)


class CeleryTaskQueueOutsideWorker(CeleryTaskQueueWorkerBase):
    """Worker implementation for Celery task queue.
    """

    def stop_worker(self):
        self._app.logger.error("Running from celery worker, kill from shell!")

    def run(self):
        self._app.logger.error("Running from celery worker, start from shell!")


class CeleryTaskQueueMainWorker(CeleryTaskQueueWorkerBase):
    """Worker implementation for Celery task queue.
    """
    def __init__(self):
        super(CeleryTaskQueueMainWorker, self).__init__()

        self.celery_worker = None

    def stop_worker(self):
        self._app.logger.info("Stopping Celery worker on demand - quitting.")
        self.celery_worker.stop()

    def run(self, argv):
        self._app.logger.info("Running the worker.")
        self.celery_worker = self.celery_app.worker_main((sys.argv[0],) + argv)


class CeleryTaskQueueMainWorkerModule(Module):
    @singleton
    @provides(CeleryTaskQueueWorkerBase)
    def provide_worker(self):
        return CeleryTaskQueueMainWorker()


class CeleryTaskQueueOutsideWorkerModule(Module):
    @singleton
    @provides(CeleryTaskQueueWorkerBase)
    def provide_worker(self):
        return CeleryTaskQueueMainWorker()


@shared_task
@inject(worker=CeleryTaskQueueWorkerBase)
def execute_task(job_data, worker):
    # type: (object, CeleryTaskQueueWorkerBase) -> dict
    return worker.execute_celery_task(job_data)


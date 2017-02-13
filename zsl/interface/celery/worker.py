import sys

from celery import Celery

from zsl import Config
from zsl.application.service_application import ServiceApplication
from zsl.utils.injection_helper import inject
from zsl.router.task import TaskRouter
from zsl.interface.task_queue import Worker, execute_task


class CeleryWorker(Worker):
    """Worker implementation for Celery task queue.
    """
    _APP_NAME = 'zsl'
    _TASK_NAME = 'execute_task'

    def __init__(self):
        super(CeleryWorker, self).__init__()

        self.celery_app = Celery(self._APP_NAME, backend='rpc', broker='redis://localhost')
        self.celery_app.task(execute_task)

    def execute_task(self, job_context):
        self._app.logger.info("Executing task.")
        return job_context.task_callable(job_context.task_data)

    def run(self, argv):
        self._app.logger.info("Running the worker.")
        self.celery_app.worker_main((sys.argv[0],) + argv)

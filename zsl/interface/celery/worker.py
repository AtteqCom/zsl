import sys

from celery import Celery

from zsl.interface.task_queue import TaskQueueWorker, execute_task


class CeleryTaskQueueWorker(TaskQueueWorker):
    """Worker implementation for Celery task queue.
    """
    _DEFAULT_APP_NAME = 'zsl'

    def __init__(self):
        super(CeleryTaskQueueWorker, self).__init__()

        self.celery_app = Celery(self._config.get('CELERY_APP_NAME', self._DEFAULT_APP_NAME), backend='rpc',
                                 broker='redis://localhost')
        self.celery_app.task(execute_task)

    def execute_task(self, job_context):
        self._app.logger.info("Executing task.")
        return job_context.task_callable(job_context.task_data)

    def run(self, argv):
        self._app.logger.info("Running the worker.")
        self.celery_app.worker_main((sys.argv[0],) + argv)

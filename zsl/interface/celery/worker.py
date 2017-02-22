import sys

from celery import Celery, shared_task
from injector import Module, singleton, provides

from zsl.interface.task_queue import TaskQueueWorker
from zsl.task.job_context import Job
from zsl.utils.injection_helper import inject


class CeleryTaskQueueWorker(TaskQueueWorker):
    """Worker implementation for Celery task queue.
    """
    _DEFAULT_APP_NAME = 'zsl'

    def __init__(self):
        super(CeleryTaskQueueWorker, self).__init__()

        self.celery_app = Celery(self._config.get('CELERY_APP_NAME', self._DEFAULT_APP_NAME), backend='rpc',
                                 broker='redis://localhost')

        self.celery_worker = None

    def stop_worker(self):
        self._app.logger.info("Stopping Celery worker on demand - quitting.")
        self.celery_worker.stop()

    def execute_celery_task(self, job_data):
        job = Job(job_data)

        return self.execute_job(job)

    def run(self, argv):
        self._app.logger.info("Running the worker.")
        self.celery_worker = self.celery_app.worker_main((sys.argv[0],) + argv)


class CeleryTaskQueueWorkerModule(Module):
    @singleton
    @provides(CeleryTaskQueueWorker)
    def provide_worker(self):
        return CeleryTaskQueueWorker()


@shared_task
@inject(worker=CeleryTaskQueueWorker)
def execute_task(job_data, worker):
    # type: (CeleryTaskExecutor) -> dict
    return worker.execute_celery_task(job_data)

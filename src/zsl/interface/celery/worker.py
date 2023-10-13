"""
:mod:`zsl.interface.celery.worker`
----------------------------------

Implementation of celery workers.

.. moduleauthor:: Peter Morihladko
"""
from celery import Celery, shared_task

from zsl import Config, Injected, inject
from zsl.interface.task_queue import JobResult, TaskQueueWorker
from zsl.task.job_context import Job, JobData


class CeleryTaskQueueWorkerBase(TaskQueueWorker):
    """Base class for celery task queue worker.

    It contains only the task execution part of worker.
    """

    def execute_celery_task(self, job_data: dict) -> JobResult:
        """Creates job from task and executes the job.

        :param job_data: job's data
        :return: job results
        :rtype: dict
        """
        job = Job(job_data)
        return self.execute_job(job)


class CeleryTaskQueueOutsideWorker(CeleryTaskQueueWorkerBase):
    """Celery worker used only for task execution.

    This can be used when the worker is managed with some other application,
    like `celery worker` or `celery multi`.
    """

    def stop_worker(self):
        self._app.logger.error("Running from celery worker, kill from shell!")

    def run(self):
        self._app.logger.error("Running from celery worker, start from shell!")


@inject(config=Config)
def create_celery_app(config: Config = Injected) -> Celery:
    celery_app = Celery()
    celery_app.config_from_object(config["CELERY"])
    return celery_app


class CeleryTaskQueueMainWorker(CeleryTaskQueueWorkerBase):
    """Worker implementation for Celery task queue."""

    def __init__(
        self,
    ):
        super().__init__()
        self.celery_app = create_celery_app()

    def stop_worker(self):
        self._app.logger.error(
            "This is a celery app worker, kill the instance to stop it."
        )

    def run(self, argv: list[str]):
        """
        Run the celery worker cmd with given arguments from the list.

        Note: the first argument should be "worker".
        """
        self._app.logger.info("Running the worker.")
        self.celery_app.worker_main(argv)


@shared_task
@inject(worker=CeleryTaskQueueWorkerBase)
def zsl_task(job_data: JobData, worker: CeleryTaskQueueWorkerBase = Injected) -> JobResult:
    """
    Executes a task registered with Celery using the provided job data.

    `job_data` is a dictionary that describes the path to the desired task along with the payload. Specifically,
    it should contain a 'path' key pointing to the task and a 'data' key with the payload as a dictionary.

    :param job_data: A dictionary containing the path to the task and its payload.
    :type job_data: dict
    :param worker: The Celery worker responsible for executing the task. *Injected.*
    :type worker: CeleryTaskQueueWorkerBase
    :return: The result of the executed task.
    :rtype: JobResult

    :Example:
    >>> job_data = {
            "path": "some_module/some_task_function",
            "data": {
                "param1": "value1",
                "param2": "value2"
            }
        }
    """
    return worker.execute_celery_task(job_data)

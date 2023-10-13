"""
:mod:`zsl.interface.task_queue`
-------------------------------

This module contains interfaces and functions to handle task queues in ZSL. A
task queue handles asynchronous and distributed code executions.

.. moduleauthor:: Peter Morihladko
"""
import abc
import socket
import traceback
from typing import Any, TypedDict

from zsl import Config, Injected, Zsl, inject
from zsl.router.task import TaskRouter
from zsl.task.job_context import Job, JobContext


class KillWorkerException(Exception):
    """If any task raises this exception a standalone worker will be killed."""

    pass


class JobResult(TypedDict):
    task_name: Any
    data: Any


@inject(app=Zsl, task_router=TaskRouter)
def execute_job(
    job: Job, app: Zsl = Injected, task_router: TaskRouter = Injected
) -> JobResult:
    """Execute a job.

    :param job: job to execute
    :type job: Job
    :param app: service application instance, injected
    :type app: ServiceApplication
    :param task_router: task router instance, injected
    :type task_router: TaskRouter
    :return: task result
    :rtype: dict
    """

    app.logger.info("Job fetched, preparing the task '{0}'.".format(job.path))

    task, task_callable = task_router.route(job.path)
    jc = JobContext(job, task, task_callable)

    app.logger.info("Executing task.")
    result = jc.task_callable(jc.task_data)

    app.logger.info("Task {0} executed successfully.".format(job.path))

    return {"task_name": job.path, "data": result}


class TaskQueueWorker(metaclass=abc.ABCMeta):
    """Task queue worker abstraction.

    A task queue worker is responsible for communicating with a task queue and
    executing any task given by it.
    It should be able to run as a stand alone application.
    """

    @inject(app=Zsl, config=Config)
    def __init__(self, app: Zsl = Injected, config: Config = Injected):
        self._app = app
        self._config = config
        self._should_stop = False

    @staticmethod
    def _get_client_id() -> str:
        """Return client id.

        :return: client id
        :rtype: str
        """
        return "zsl-client-{0}".format(socket.gethostname())

    def handle_exception(self, e: Exception, task_path: str) -> JobResult:
        """Handle exception raised during task execution.

        :param e: exception
        :type e: Exception
        :param task_path: task path
        :type task_path: str
        :return: exception as task result
        :rtype: dict
        """

        self._app.logger.error(str(e) + "\n" + traceback.format_exc())
        return {"task_name": task_path, "data": None, "error": str(e)}

    def execute_job(self, job: Job) -> JobResult:
        """Execute job given by the task queue.

        :param job: job
        :type job: Job
        :return: task result
        :rtype: dict
        """
        try:
            return execute_job(job)

        except KillWorkerException:
            self._app.logger.info("Stopping Gearman worker on demand flag set.")
            self.stop_worker()

        except Exception as e:
            return self.handle_exception(e, job.path)

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        """Run the worker."""
        pass

    @abc.abstractmethod
    def stop_worker(self):
        """Stop the worker."""
        pass


@inject(worker=TaskQueueWorker)
def _get_worker(worker: TaskQueueWorker = Injected) -> TaskQueueWorker:
    return worker


def run_worker(*args: Any, **kwargs: Any) -> None:
    """Run the app as a task queue worker.

    The worker instance is given as a DI module.
    """
    worker = _get_worker()
    worker.run(*args, **kwargs)

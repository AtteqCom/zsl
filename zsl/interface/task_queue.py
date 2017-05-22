"""
:mod:`zsl.interface.task_queue`
-------------------------------

This module contains interfaces and functions to handle task queues in ZSL. A
task queue handles asynchronous and distributed code executions.

.. moduleauthor:: Peter Morihladko
"""
from future.utils import with_metaclass

import abc
import traceback
import socket

from zsl import Zsl, Config, Injected
from zsl import inject
from zsl.router.task import TaskRouter
from zsl.task.job_context import JobContext, Job


class KillWorkerException(Exception):
    """If any task raises this exception a standalone worker will be killed."""
    pass


@inject(app=Zsl, task_router=TaskRouter)
def execute_job(job, app=Injected, task_router=Injected):
    # type: (Job, Zsl, TaskRouter) -> dict
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
    JobContext.set_current_context(jc)

    app.logger.info("Executing task.")
    result = jc.task_callable(jc.task_data)

    app.logger.info("Task {0} executed successfully.".format(job.path))

    return {'task_name': job.path, 'data': result}


class TaskQueueWorker(with_metaclass(abc.ABCMeta, object)):
    """Task queue worker abstraction.

    A task queue worker is responsible for communicating with a task queue and
    executing any task given by it.
    It should be able to run as a stand alone application.
    """

    @inject(app=Zsl, config=Config, task_router=TaskRouter)
    def __init__(self, app, config, task_router):
        # type: (Zsl, Config, TaskRouter) -> None
        self._app = app
        self._config = config
        self._task_router = task_router

        self._should_stop = False

        self._task_router.set_task_reloading(self._task_router.is_task_reloading() or self._config['RELOAD_GEARMAN'])

    @staticmethod
    def _get_client_id():
        # type: () -> str
        """Return client id.

        :return: client id
        :rtype: str
        """
        return "zsl-client-{0}".format(socket.gethostname())

    def handle_exception(self, e, task_path):
        # type: (Exception, str) -> dict
        """Handle exception raised during task execution.

        :param e: exception
        :type e: Exception
        :param task_path: task path
        :type task_path: str
        :return: exception as task result
        :rtype: dict
        """

        self._app.logger.error(str(e) + "\n" + traceback.format_exc())
        return {'task_name': task_path, 'data': None, 'error': str(e)}

    def execute_job(self, job):
        # type: (Job) -> dict
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

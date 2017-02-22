from future.utils import with_metaclass

import abc
import traceback
import socket

from zsl.application.service_application import ServiceApplication
from zsl import Config
from zsl.utils.injection_helper import inject
from zsl.router import task_router
from zsl.task.job_context import JobContext, Job


class KillWorkerException(Exception):
    pass


@inject(app=ServiceApplication)
def execute_job(job, app):
    # type: (Job, ServiceApplication) -> dict

    app.logger.info("Job fetched, preparing the task '{0}'.".format(job.path))

    task, task_callable = task_router.route(job.path)
    jc = JobContext(job, task, task_callable)
    JobContext.set_current_context(jc)

    app.logger.info("Executing task.")
    result = jc.task_callable(jc.task_data)

    app.logger.info("Task {0} executed successfully.".format(job.path))

    return {'task_name': job.path, 'data': result}


class TaskQueueWorker(with_metaclass(abc.ABCMeta, object)):
    """Class responsible for connecting to the Gearman server and grabbing
    tasks. Then uses task to get the task object and executes it.
    """

    @inject(app=ServiceApplication, config=Config)
    def __init__(self, app, config):
        # type: (ServiceApplication, Config) -> None
        self._app = app
        self._config = config
        self._task_router = task_router

        self._should_stop = False

        self._task_router.set_task_reloading(
            self._task_router.is_task_reloading() or self._config['RELOAD_GEARMAN'])

    @staticmethod
    def _get_client_id():
        return "zsl-client-{0}".format(socket.gethostname())

    def handle_exception(self, e, task_path):
        self._app.logger.error(str(e) + "\n" + traceback.format_exc())
        return {'task_name': task_path, 'data': None, 'error': str(e)}

    def execute_job(self, job):
        # type: (Job) -> dict
        """

        :param job:
        :return:
        """
        try:
            return execute_job(job)

        except KillWorkerException:
            self._app.logger.info("Stopping Gearman worker on demand flag set.")
            self.stop_worker()

        except Exception as e:
            return self.handle_exception(e, job.path)

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def stop_worker(self):
        pass





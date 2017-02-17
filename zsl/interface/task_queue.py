from future.utils import with_metaclass

import abc
import traceback
import socket

from zsl.application.service_application import ServiceApplication
from zsl import Config
from zsl.utils.injection_helper import inject
from zsl.router import task_router
from zsl.task.job_context import JobContext


class KillWorkerException(Exception):
    pass


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

    @abc.abstractmethod
    def execute_task(self, job_context):
        pass

    @abc.abstractmethod
    def run(self):
        pass


@inject(app=ServiceApplication)
def execute_task(worker, job, app):
    # type: (ReloadingWorker, GearmanJob, ServiceApplication) -> None

    app.logger.info("Job fetched, preparing the task '{0}'.".format(job.data['path']))

    try:
        (task, task_callable) = task_router.route(job.data['path'])
        jc = JobContext(job, task, task_callable)
        JobContext.set_current_context(jc)
        data = worker.logical_worker.execute_task(jc)
        app.logger.info("Task {0} executed successfully.".format(job.data['path']))
        return {'task_name': job.data['path'], 'data': data}
    except KillWorkerException as e:
        app.logger.info("Stopping Gearman worker on demand flag set.")
        worker._should_stop = True
    except Exception as e:
        app.logger.error(str(e) + "\n" + traceback.format_exc())
        return {'task_name': job.data['path'], 'data': None, 'error': str(e)}



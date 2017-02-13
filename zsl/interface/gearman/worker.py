"""
:mod:`zsl.interface.gearman.worker`
-----------------------------------

.. moduleauthor:: Martin
"""
from __future__ import unicode_literals
import gearman

from zsl import inject, Config
from zsl.application.service_application import ServiceApplication
from zsl.router.task import TaskRouter
from zsl.interface.task_queue import Worker, execute_task
from zsl.interface.gearman.json_data_encoder import JSONDataEncoder


class ReloadingWorker(gearman.GearmanWorker):
    def __init__(self, host_list=None):
        super(ReloadingWorker, self).__init__(host_list)
        self._should_stop = False

    def on_job_complete(self, current_job, job_result):
        super(ReloadingWorker, self).on_job_complete(current_job, job_result)
        if self._should_stop:
            app.logger.info("Stopping Gearman worker on demand - quitting.")
            quit()
        return True


class GearmanWorker(Worker):
    def __init__(self):
        super(GearmanWorker, self).__init__()

        self.gearman_worker = ReloadingWorker(
            ["{0}:{1}".format(self._config['GEARMAN']['host'],
                              self._config['GEARMAN']['port'])])
        self.gearman_worker.set_client_id(self._get_client_id())
        self.gearman_worker.data_encoder = JSONDataEncoder
        self.gearman_worker.register_task(self._config['GEARMAN_TASK_NAME'], execute_task)
        self.gearman_worker.logical_worker = self

    def execute_task(self, job_context):
        self._app.logger.info("Executing task.")
        return job_context.task_callable(job_context.task_data)

    def run(self):
        self._app.logger.info("Running the worker.")
        self.gearman_worker.work()

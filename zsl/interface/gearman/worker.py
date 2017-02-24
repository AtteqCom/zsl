"""
:mod:`zsl.interface.gearman.worker`
-----------------------------------

.. moduleauthor:: Martin
"""
from __future__ import unicode_literals
import gearman
from gearman.job import GearmanJob

from zsl.interface.task_queue import TaskQueueWorker
from zsl.task.job_context import Job
from zsl.interface.gearman.json_data_encoder import JSONDataEncoder


class ReloadingWorker(gearman.GearmanWorker):
    def __init__(self, host_list=None):
        super(ReloadingWorker, self).__init__(host_list)
        self._should_stop = False

    def on_job_complete(self, current_job, job_result):
        super(ReloadingWorker, self).on_job_complete(current_job, job_result)
        if self._should_stop:
            quit()
        return True


def job_from_gearman_job(gearman_job):
    # type: (GearmanJob) -> Job
    """Creates zsl job from gearman job.

    :param gearman_job: gearman job
    :type gearman_job: GearmanJob
    :return: zsl job
    :rtype: Job
    """

    return Job(gearman_job.data)


class GearmanTaskQueueWorker(TaskQueueWorker):
    def __init__(self):
        super(GearmanTaskQueueWorker, self).__init__()

        self.gearman_worker = ReloadingWorker(
            ["{0}:{1}".format(self._config['GEARMAN']['host'],
                              self._config['GEARMAN']['port'])])
        self.gearman_worker.set_client_id(self._get_client_id())
        self.gearman_worker.data_encoder = JSONDataEncoder
        self.gearman_worker.register_task(self._config['GEARMAN_TASK_NAME'], self.execute_gearman_job)
        self.gearman_worker.logical_worker = self

        self._current_worker = None

    def stop_worker(self):
        self._app.logger.info("Stopping Gearman worker on demand - quitting.")
        self._current_worker._should_stop = True

    def execute_gearman_job(self, worker, job):
        # type: (ReloadingWorker, GearmanJob) -> dict
        job = job_from_gearman_job(job)
        self._current_worker = worker

        return self.execute_job(job)

    def run(self):
        self._app.logger.info("Running the worker.")
        self.gearman_worker.work()

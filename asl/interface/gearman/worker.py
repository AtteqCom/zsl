'''
Created on 12.12.2012

@author: Martin
'''

from asl.application.service_application import service_application
from asl.router import router
import gearman
from asl.interface.gearman.json_data_encoder import JSONDataEncoder
from asl.task.task_data import TaskData
import socket
from asl.task.job_context import JobContext

app = service_application

def executeTask(worker, job):
    print "Job fetched, preparing the task."
    
    try:
        (task, task_callable) = router.route(job.data['path'])
        jc = JobContext(job, task, task_callable)
        JobContext.set_current_context(jc)
        data = worker.logical_worker.executeTask(jc)
        app.logger.info("Task {0} executed successfully.".format(job.data['path']))
        return {'task_name': job.data['path'], 'data': data}
    except Exception as e:
        app.logger.error(str(e))
        return {'task_name': job.data['path'], 'data': None, 'error': str(e)}

'''
Class responsible for connecting to the Gearman server and grabbing tasks.
Then uses router to get the task object and executes it.
'''
class Worker:
    def __init__(self, app):
        self._app = app
        router.set_task_reloading(router.is_task_reloading() or app.config['RELOAD_GEARMAN'])
        self.gearman_worker = gearman.GearmanWorker(["{0}:{1}".format(app.config['GEARMAN']['host'], app.config['GEARMAN']['port'])])
        self.gearman_worker.set_client_id("asl-client-{}".format(socket.gethostname()))
        self.gearman_worker.data_encoder = JSONDataEncoder
        self.gearman_worker.register_task(self._app.config['GEARMAN_TASK_NAME'], executeTask)
        self.gearman_worker.logical_worker = self

    def executeTask(self, job_context):
        self._app.logger.info("Executing task.")
        return job_context.task_callable(job_context.task_data)

    def run(self):
        self._app.logger.info("Running the worker.")
        self.gearman_worker.work()

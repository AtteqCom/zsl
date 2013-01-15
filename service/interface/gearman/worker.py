'''
Created on 12.12.2012

@author: Martin
'''

from application.service_application import service_application
from router import router
import gearman
import interface.gearman
from interface.gearman.json_data_encoder import JSONDataEncoder
from task.task_data import TaskData
import socket

app = service_application

def executeTask(worker, job):
    print "Job fetched, preparing the task."
    try:
        (task, task_callable) = router.route(job.data['path'])
        data = worker.logical_worker.executeTask(task, task_callable, job.data['data'])
        print "Task {0} executed successfully.".format(job.data['path'])
        return {'task_name': job.data['path'], 'data': data}
    except Exception as e:
        return {'task_name': job.data['path'], 'data': None, 'error': str(e0)}
        print e

'''
Class responsible for connecting to the Gearman server and grabbing tasks.
Then uses router to get the task object and executes it.
'''
class Worker:
    def __init__(self, app):
        self.app = app
        self.app.initialize_dependencies()

        router.set_task_reloading(router.is_task_reloading() or app.config['RELOAD_GEARMAN'])
        self.gearman_worker = gearman.GearmanWorker(["{0}:{1}".format(app.config['GEARMAN']['host'], app.config['GEARMAN']['port'])])
        self.gearman_worker.set_client_id("sportky-client-%s".format(socket.gethostname()))
        self.gearman_worker.data_encoder = JSONDataEncoder
        self.gearman_worker.register_task(interface.gearman.SPORTKY_TASK_NAME, executeTask)
        self.gearman_worker.logical_worker = self

    def executeTask(self, task, task_callable, data):
        print "Executing task."
        return task_callable(TaskData(app, data))

    def run(self):
        print "Running the worker."
        self.gearman_worker.work()

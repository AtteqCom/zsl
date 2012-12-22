'''
Created on 12.12.2012

@author: Martin
'''

from application.service_application import service_application
from router import router
import gearman
from interface.gearman.json_data_encoder import JSONDataEncoder
from task.task_data import TaskData

app = service_application

def executeTask(worker, job):
    print "Job fetched, preparing the task."
    try:
        (task, task_callable) = router.route(job.data['path'])
        data = worker.logical_worker.executeTask(task, task_callable, job.data['data'])
        print "Executed successfully, return value '{0}'.".format(data)
        return {'task_name': job.data['path'], 'data': data}
    except Exception as e:
        print e

'''
Class responsible for connecting to the Gearman server and grabbing tasks.
Then uses router to get the task object and executes it.
'''
class Worker:
    def __init__(self, app):
        self.app = app
        self.gearman_worker = gearman.GearmanWorker(["{0}:{1}".format(app.config['GEARMAN']['host'], app.config['GEARMAN']['port'])])
        self.gearman_worker.set_client_id('client_id')
        self.gearman_worker.data_encoder = JSONDataEncoder
        self.gearman_worker.register_task('task', executeTask)
        self.gearman_worker.logical_worker = self

    def executeTask(self, task, task_callable, data):
        print "Executing task."
        return task_callable(TaskData(app, data))

    def run(self):
        print "Running the worker."
        self.gearman_worker.work()

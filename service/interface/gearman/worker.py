'''
Created on 12.12.2012

@author: Martin
'''

from application.service_application import service_application
import gearman

app = service_application

'''
Class responsible for connecting to the Gearman server and grabbing tasks.
Then uses router to get the task object and executes it.
'''
class Worker:
    def __init__(self, app):
        self.app = app
        self.gearman_client = gearman.GearmanClient(["{0}:{1}".format(app.config['GEARMAN']['host'], app.config['GEARMAN']['port'])])

    def run(self):
        while True:
            try:
                t = self.fetchTask()
                self.executeTask(t)
            except Exception as e:
                app.logger.error(e)

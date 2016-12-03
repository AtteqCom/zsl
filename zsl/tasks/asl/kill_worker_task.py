'''
Created on 22.12.2012

@author: Martin Babka
'''

from zsl.application.service_application import AtteqServiceFlask
from injector import inject
from zsl.task.job_context import JobContext, WebJobContext
from zsl.interface.gearman.worker import KillWorkerException

class KillWorkerTask(object):

    @inject(app=AtteqServiceFlask)
    def __init__(self, app):
        self._app = app

    def perform(self, data):
        if isinstance(JobContext.get_current_context(), WebJobContext):
            raise Exception("Can not kill worker from web!")
        
        raise KillWorkerException()

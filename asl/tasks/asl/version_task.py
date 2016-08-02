'''
Created on 24.12.2012

@author: Martin Babka
'''

from asl.application.service_application import service_application
from asl.task.task_decorator import json_output
import sqlalchemy


class VersionTask(object):
    '''
    Shows the versions of ASL and the various used libraries.
    '''

    @json_output
    def perform(self, data):
        return {
            "ASL": service_application.VERSION,
            "SqlAlchemy": sqlalchemy.__version__
        }

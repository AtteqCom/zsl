"""
:mod:`zsl.tasks.asl.version_task`
---------------------------------

Created on 24.12.2012

..moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

from builtins import object
from zsl.application.service_application import service_application
from zsl.task.task_decorator import json_output
import sqlalchemy


class VersionTask(object):
    """
    Shows the versions of ASL and the various used libraries.
    """

    @json_output
    def perform(self, data):
        return {
            "ASL": service_application.VERSION,
            "SqlAlchemy": sqlalchemy.__version__
        }

"""
:mod:`zsl.tasks.asl.version_task`
---------------------------------

Created on 24.12.2012

..moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

from builtins import object

import sqlalchemy

from zsl import Zsl, inject
from zsl.task.task_decorator import json_output


class VersionTask(object):
    """
    Shows the versions of ASL and the various used libraries.
    """

    @inject(app=Zsl)
    def __init__(self, app):
        self._app = app

    @json_output
    def perform(self, data):
        return {
            "ASL": self._app.VERSION,
            "SqlAlchemy": sqlalchemy.__version__
        }

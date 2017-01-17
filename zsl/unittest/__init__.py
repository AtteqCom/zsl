"""
:mod:`zsl.unittest`
-------------------
"""

from __future__ import unicode_literals
from zsl.interface.importer import initialize_cli_application, InitializationContext
import unittest
import json

initialize_cli_application(InitializationContext(unit_test=True))

from zsl.task.task_data import TaskData
from zsl.utils.injection_helper import inject
from zsl.application.service_application import AtteqServiceFlask
from sqlalchemy.engine.base import Engine
from zsl.db.model.sql_alchemy import metadata


class TestCase(unittest.TestCase):
    @inject(engine=Engine)
    def createSchema(self, engine):
        metadata.create_all(engine)


class TestTaskData(TaskData):
    @inject(service_application=AtteqServiceFlask)
    def __init__(self, data, service_application):
        TaskData.__init__(self, service_application, json.dumps(data))

"""
:mod:`zsl.unittest`
-------------------
"""

from __future__ import unicode_literals
from __future__ import absolute_import

import unittest
import json


from zsl.task.task_data import TaskData
from zsl import inject
from sqlalchemy.engine.base import Engine
from zsl.db.model.sql_alchemy import metadata


class TestCase(unittest.TestCase):
    @inject(engine=Engine)
    def createSchema(self, engine):
        metadata.bind = engine
        metadata.create_all(engine)


class TestTaskData(TaskData):
    def __init__(self, data):
        super(TestTaskData, self).__init__(json.dumps(data))

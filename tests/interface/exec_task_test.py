from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *  # NOQA
from typing import Callable
from unittest.case import TestCase

from zsl.application.containers.web_container import WebContainer
from zsl.errors import ZslError
from zsl.interface.task import create_task
from zsl.tasks.zsl.version_task import VersionTask
from zsl.testing.db import IN_MEMORY_DB_SETTINGS
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration


class ExecTaskTestCase(ZslTestCase, TestCase):
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name='ExecTaskTestCase', container=WebContainer,
        config_object=IN_MEMORY_DB_SETTINGS)

    def testCreateTaskNone(self):
        with self.assertRaises(ZslError):
            create_task(None)

    def testCreateTaskValidCls(self):
        task, task_callable = create_task(VersionTask)
        self.assertIsInstance(task, VersionTask,
                              "A proper task must be returned.")
        self.assertIsInstance(task_callable, Callable,
                              "A proper callable must be returned.")

    def testCreateTaskValidPath(self):
        task, task_callable = create_task("task/zsl/version_task")
        self.assertIsInstance(task, VersionTask,
                              "A proper task must be returned.")
        self.assertIsInstance(task_callable, Callable,
                              "A proper callable must be returned.")

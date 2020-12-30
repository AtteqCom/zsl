import http.client
from unittest.case import TestCase

from zsl import Zsl, inject
from zsl.application.containers.core_container import CoreContainer
from zsl.router.task import TaskConfiguration
from zsl.testing.db import IN_MEMORY_DB_SETTINGS
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration


class AppVersionTestCase(ZslTestCase, TestCase):
    CONFIG = IN_MEMORY_DB_SETTINGS.copy()
    CONFIG.update(
        TASKS=TaskConfiguration()
    )
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name='ErrorHandlingTestCase', container=CoreContainer,
        version="1234.1111.4321",
        config_object=CONFIG)

    @inject(app=Zsl)
    def testErrorTaskExecution(self, app: Zsl) -> None:
        self.assertEqual(Zsl.VERSION, app.zsl_version)
        self.assertEqual("1234.1111.4321", app.app_version)
        self.assertEqual(Zsl.VERSION + ":1234.1111.4321", app.get_version())
        self.assertEqual(Zsl.VERSION + ":1234.1111.4321", app.version)


class NoAppVersionTestCase(ZslTestCase, TestCase):
    CONFIG = IN_MEMORY_DB_SETTINGS.copy()
    CONFIG.update(
        TASKS=TaskConfiguration()
    )
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name='ErrorHandlingTestCase', container=CoreContainer,
        config_object=CONFIG)

    @inject(app=Zsl)
    def testErrorTaskExecution(self, app: Zsl) -> None:
        self.assertEqual(Zsl.VERSION, app.zsl_version)
        self.assertIsNone(app.app_version)
        self.assertEqual(Zsl.VERSION, app.get_version())
        self.assertEqual(Zsl.VERSION, app.version)

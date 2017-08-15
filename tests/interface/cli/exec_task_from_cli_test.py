from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
from unittest.case import TestCase

from click.testing import CliRunner

from zsl import inject
from zsl.application.containers.core_container import CoreContainer
from zsl.application.modules.cli_module import ZslCli
from zsl.router.task import TaskConfiguration
from zsl.testing.db import IN_MEMORY_DB_SETTINGS
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration


class TestCliContainer(CoreContainer):
    pass


CONFIG = IN_MEMORY_DB_SETTINGS.copy()
CONFIG.update(
    TASKS=TaskConfiguration().create_namespace('task').add_packages(['zsl.tasks']).get_configuration()
)


class ExecTaskFromCliTestCase(ZslTestCase, TestCase):
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name="ExecTaskFromCliTestCase",
        config_object=CONFIG,
        container=TestCliContainer
    )

    @inject(zsl_cli=ZslCli)
    def testRunningTestTask(self, zsl_cli):
        # type:(ZslCli)->None
        runner = CliRunner()
        result = runner.invoke(zsl_cli.cli, ['task', 'task/zsl/test_task'])
        self.assertEqual(0, result.exit_code, "No error is expected.")
        self.assertEqual('ok', result.output.strip(), "Valid task output must be shown")

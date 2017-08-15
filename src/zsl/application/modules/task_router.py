"""
:mod:`zsl.application.modules.task_router_module`
-------------------------------------------------
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import *

from injector import ClassProvider
from injector import Module
from injector import provides
from injector import singleton

from zsl import Config
from zsl import inject
from zsl.router.task import TASK_CONFIGURATION_NAME
from zsl.router.task import TaskConfiguration
from zsl.router.task import TaskRouter


class TaskRouterModule(Module):
    """Adds task router to current configuration."""
    task_provider = ClassProvider(TaskRouter)

    @provides(interface=TaskConfiguration, scope=singleton)
    @inject(config=Config)
    def provide_task_configuration(self, config):
        default_config = self._create_default_configuration()
        return config.get(TASK_CONFIGURATION_NAME, default_config)

    def configure(self, binder):
        binder.bind(TaskRouter, to=self.task_provider, scope=singleton)

    def _create_default_configuration(self):
        return TaskConfiguration().create_namespace('task').add_packages(['zsl.tasks']).get_configuration()

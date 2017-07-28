"""
:mod:`zsl.application.modules.task_router_module`
-------------------------------------------------
"""
from __future__ import unicode_literals

from injector import Module, singleton, ClassProvider, provides

from zsl import inject, Config
from zsl.router.task import TaskRouter, TaskConfiguration, TASK_CONFIGURATION_NAME


class TaskRouterModule(Module):
    """Adds task router to current configuration."""
    task_provider = ClassProvider(TaskRouter)

    @provides(interface=TaskConfiguration, scope=singleton)
    @inject(config=Config)
    def provide_task_configuration(self, config):
        default_config = TaskConfiguration().create_namespace('task').add_packages(['zsl.tasks']).get_configuration()
        return config.get(TASK_CONFIGURATION_NAME, default_config)

    def configure(self, binder):
        binder.bind(TaskRouter, to=self.task_provider, scope=singleton)

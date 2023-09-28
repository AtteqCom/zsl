"""
:mod:`zsl.application.modules.task_router_module`
-------------------------------------------------
"""
from injector import ClassProvider, Module, provides, singleton

from zsl import Config, inject
from zsl.router.task import TASK_CONFIGURATION_NAME, TaskConfiguration, TaskRouter


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

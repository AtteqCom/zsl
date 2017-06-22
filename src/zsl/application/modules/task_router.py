"""
:mod:`zsl.application.modules.task_router_module`
-------------------------------------------------
"""
from __future__ import unicode_literals

from injector import Module, singleton, ClassProvider

from zsl.router.task import TaskRouter


class TaskRouterModule(Module):
    """Adds task router to current configuration."""
    task_provider = ClassProvider(TaskRouter)

    def configure(self, binder):
        binder.bind(TaskRouter, to=self.task_provider, scope=singleton)

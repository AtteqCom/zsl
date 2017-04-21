"""
:mod:`zsl.application.modules.gearman_module`
---------------------------------------------
"""
from __future__ import unicode_literals

from injector import Module, ClassProvider, singleton
from zsl.interface.task_queue import TaskQueueWorker
from zsl.interface.gearman.worker import GearmanTaskQueueWorker


class GearmanModule(Module):
    """Adds gearman to current configuration."""
    def configure(self, binder):
        binder.bind(TaskQueueWorker, to=ClassProvider(GearmanTaskQueueWorker), scope=singleton)

"""
:mod:`zsl.application.modules.celery_module`
--------------------------------------------
"""
from __future__ import unicode_literals

from injector import Module, singleton

from zsl.interface.task_queue import TaskQueueWorker
from zsl.interface.celery.worker import CeleryTaskQueueWorkerBase, CeleryTaskQueueMainWorker,\
    CeleryTaskQueueOutsideWorker


class CeleryTaskQueueMainWorkerModule(Module):
    """Adds celery worker to current configuration."""
    def configure(self, binder):
        worker = CeleryTaskQueueMainWorker()
        binder.bind(TaskQueueWorker, to=worker, scope=singleton)
        binder.bind(CeleryTaskQueueWorkerBase, to=worker, scope=singleton)


class CeleryTaskQueueOutsideWorkerModule(Module):
    """Adds celery outside worker to current configuration.

    Outside worker is meant to run with help of celery cli tools.
    """
    def configure(self, binder):
        worker = CeleryTaskQueueOutsideWorker()
        binder.bind(TaskQueueWorker, to=worker, scope=singleton)
        binder.bind(CeleryTaskQueueWorkerBase, to=worker, scope=singleton)

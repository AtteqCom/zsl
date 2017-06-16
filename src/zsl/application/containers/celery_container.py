"""
:mod:`zsl.application.containers.celery_container`
--------------------------------------------------
"""
from __future__ import unicode_literals

from zsl.application.containers.core_container import CoreContainer
from zsl.application.modules.celery_module import CeleryTaskQueueOutsideWorkerModule, CeleryTaskQueueMainWorkerModule, \
    CeleryCliModule


class CeleryContainer(CoreContainer):
    """Configuration for celery application."""
    worker = CeleryTaskQueueMainWorkerModule
    celery_cli = CeleryCliModule


class CeleryStandAloneContainer(CoreContainer):
    """Configuration for application run with help of celery cli tools."""
    worker = CeleryTaskQueueOutsideWorkerModule
    celery_cli = CeleryCliModule

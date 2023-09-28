"""
:mod:`zsl.application.containers.gearman_container`
---------------------------------------------------
"""
from zsl.application.containers.core_container import CoreContainer
from zsl.application.modules.gearman_module import GearmanModule


class GearmanContainer(CoreContainer):
    """Configuration for Gearman application."""
    worker = GearmanModule

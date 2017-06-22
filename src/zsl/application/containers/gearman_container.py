"""
:mod:`zsl.application.containers.gearman_container`
---------------------------------------------------
"""
from __future__ import unicode_literals

from zsl.application.containers.core_container import CoreContainer
from zsl.application.modules.gearman_module import GearmanModule


class GearmanContainer(CoreContainer):
    """Configuration for Gearman application."""
    worker = GearmanModule

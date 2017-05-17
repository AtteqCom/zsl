"""
:mod:`zsl.application.containers.core_container`
------------------------------------------------
"""
from __future__ import unicode_literals

from zsl.application.containers.container import IoCContainer
from zsl.application.modules.cli_module import CliModule
from zsl.application.modules.logger_module import LoggerModule
from zsl.application.modules.alchemy_module import AlchemyModule
from zsl.application.modules.cache_module import RedisCacheInjectionModule
from zsl.application.modules.context_module import DefaultContextModule
from zsl.application.modules.task_router import TaskRouterModule


class CoreContainer(IoCContainer):
    """Modules for basic Zsl application."""
    logger = LoggerModule
    database = AlchemyModule
    cache = RedisCacheInjectionModule
    context = DefaultContextModule
    task_router = TaskRouterModule
    cli = CliModule

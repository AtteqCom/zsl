"""
:mod:`zsl.application.modules.context_module`
---------------------------------------------

Application context describes the environment in which the application is run\
and is responsible for specific initializations on it.
"""
from __future__ import unicode_literals

from zsl.application.initialization_context import InitializationContext
from injector import singleton, Module

from zsl.application.initializers.library_initializer import LibraryInitializer
from zsl.application.initializers.service_initializer import ServiceInitializer
from zsl.application.initializers.unittest_initializer import UnitTestInitializer
from zsl.application.initializers.web_initializer import WebInitializer

#: Initializers used in all applications
default_initializers = (LibraryInitializer, ServiceInitializer)

#: Initializers used in unit test applications
unittest_initializers = default_initializers + (UnitTestInitializer,)

#: Initializers used in unit web applications
web_initializers = default_initializers + (WebInitializer,)


class DefaultContextModule(Module):
    """Adds default application context to current configuration."""
    def _create_context(self):
        return InitializationContext(initializers=default_initializers)

    def configure(self, binder):
        context = self._create_context()
        binder.bind(InitializationContext, to=context, scope=singleton)


class WebContextModule(DefaultContextModule):
    """Adds web application context to current configuration."""
    def _create_context(self):
        return InitializationContext(initializers=web_initializers)


class WorkerContextModule(DefaultContextModule):
    """Worker application context to current configuration."""
    pass


class TestContextModule(DefaultContextModule):
    """Test application context to current configuration"""
    def _create_context(self):
        return InitializationContext(unit_test=True, initializers=unittest_initializers)

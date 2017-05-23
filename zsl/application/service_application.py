"""
:mod:`zsl.application.service_application`
------------------------------------------
"""
from __future__ import unicode_literals

import os
from typing import Callable

from flask import Flask, Config
from flask_injector import FlaskInjector
from injector import Injector, Binder, singleton

from zsl import __version__
from zsl._state import set_current_app
from zsl.utils.warnings import deprecated
from zsl.application.initialization_context import InitializationContext


class ServiceApplication(Flask):
    """Atteq Service Flask application."""

    VERSION = __version__

    def __init__(self, import_name, static_path=None, static_url_path=None,
                 static_folder='static', template_folder='templates',
                 instance_path=None, instance_relative_config=False,
                 modules=None, config_object=None, version=None):
        super(ServiceApplication, self).__init__(import_name, static_path, static_url_path,
                                                 static_folder, template_folder, instance_path,
                                                 instance_relative_config)
        self._dependencies_initialized = False
        self._is_initialized = False
        self._injector = None
        self._worker = None
        self._configure(config_object)
        self._app_version = version
        if not modules:
            from zsl.application.containers.core_container import CoreContainer
            modules = CoreContainer.modules()
        self._configure_injector(modules)
        self._initialize()
        self._dependencies_initialized = True

    def __str__(self):
        return "ZSL(application={0}, zsl_version={1}, app_version={2})".format(self.name, self.VERSION,
                                                                               self._app_version)

    def _configure(self, config_object=None):
        # type: (dict) -> None
        """Read the configuration from config files."""

        if config_object:
            self.config.from_mapping(config_object)
        else:
            self.config.from_object('settings.default_settings')

        zsl_settings = os.environ.get('ZSL_SETTINGS')
        if zsl_settings is not None:
            self.config.from_envvar('ZSL_SETTINGS')

    def _initialize(self):
        """Run the initializers."""
        ctx = self.injector.get(InitializationContext)
        ctx.initialize()

    def _register(self):
        """Register the current instance into application stack."""
        set_current_app(self)

    def _get_app_module(self):
        # type: () -> Callable
        """Returns a module which binds the current app and configuration.

        :return: configuration callback
        :rtype: Callable
        """

        def configure(binder):
            # type: (Binder) -> Callable
            binder.bind(ServiceApplication, to=self, scope=singleton)
            binder.bind(Config, to=self.config, scope=singleton)

        return configure

    def _configure_injector(self, modules):
        """Create the injector and install the modules.

        There is a necessary order of calls. First we have to bind `Config` and
        `Zsl`, then we need to register the app into the global stack and then
        we can install all other modules, which can use `Zsl` and `Config`
        injection.

        :param modules: list of injection modules
        :type modules: list
        """
        self._flask_injector = FlaskInjector(self, [self._get_app_module()])
        self.injector = self._flask_injector.injector

        self._register()

        for module in modules:
            self.injector.binder.install(module)

        self.logger.debug("Injector configuration {0}.".format(modules))
        self._dependencies_initialized = True

    @deprecated
    def get_initialization_context(self):
        return self.injector.get(InitializationContext)

    def is_initialized(self):
        return self._dependencies_initialized

    @property
    def injector(self):
        # type: () -> Injector
        return self._injector

    @injector.setter
    def injector(self, value):
        self._injector = value

    @deprecated
    def get_injector(self):
        # type: () -> Injector
        return self.injector

    @deprecated
    def set_injector(self, injector):
        self.injector = injector

    def get_version(self):
        v = self.config.get('VERSION')
        if v is None:
            return ServiceApplication.VERSION
        else:
            return ServiceApplication.VERSION + ":" + v

    @deprecated
    def run_web(self, host='127.0.0.1', port=5000, **options):
        return self.run(
            host=self.config.get('FLASK_HOST', host),
            port=self.config.get('FLASK_PORT', port),
            debug=self.config.get('DEBUG', False),
            **options
        )

    """Alias for Flask.run"""

    def run_worker(self, *args, **kwargs):
        """Run the app as a task queue worker.

        The worker instance is given as a DI module.
        """
        from zsl.interface.task_queue import TaskQueueWorker
        worker = self.injector.get(TaskQueueWorker)
        worker.run(*args, **kwargs)

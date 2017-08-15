"""
:mod:`zsl.application.service_application`
------------------------------------------

The module contains the main Zsl class - :class:`.ServiceApplication`. It is
responsible for gluing everything together.

There is a simple profile support. Profile is usually tied to a configuration
file for an environment. Usually environments slightly differ in settings -
especially connection strings. These twists can be managed via additional
configuration files with the `cfg` extension usually placed in the `settings`
package. The name of the environment configuration file is controlled via
`ZSL_SETTINGS` environment variable.


.. data:: SETTINGS_ENV_VAR_NAME

    Name of the environment variable to be read for the profile configuration
    file.

"""
from __future__ import unicode_literals

import os
from typing import Any, Callable

from flask import Config, Flask
from injector import Binder, Injector, singleton

from zsl._state import set_current_app
from zsl.application.initialization_context import InitializationContext
from zsl.utils.warnings import deprecated
from zsl.version import version

#: Name of the environment variable to be read for the profile configuration.
SETTINGS_ENV_VAR_NAME = 'ZSL_SETTINGS'


def get_settings_from_profile(profile, profile_dir=None):
    # type: (str, Any)->str
    """"Returns the  configuration file path for the given profile.

    :param profile: Profile name to be used.
    :param profile_dir: The directory where the profile configuration file should reside. It
                        may be also a module, and then the directory of the module is used.
    :return: Configuration file path.
    """
    if profile_dir is None:
        import settings
        profile_dir = settings

    if hasattr(profile_dir, '__file__'):
        profile_dir = os.path.dirname(profile_dir.__file__)

    return os.path.join(profile_dir, '{0}.cfg'.format(profile))


def set_profile(profile):
    # type (str)->None
    """Sets the current profile.

    :param profile: The profile to be used."""
    os.environ[SETTINGS_ENV_VAR_NAME] = get_settings_from_profile(profile)


class ServiceApplication(Flask):
    """Atteq Service Flask application."""

    VERSION = version

    def __init__(self, import_name, static_path=None, static_url_path=None,
                 static_folder='static', template_folder='templates',
                 instance_path=None, instance_relative_config=False,
                 modules=None, config_object=None, version=None,
                 default_settings_module='settings.default_settings'):
        super(ServiceApplication, self).__init__(import_name, static_path,
                                                 static_url_path,
                                                 static_folder, template_folder,
                                                 instance_path,
                                                 instance_relative_config)
        self._dependencies_initialized = False
        self._default_settings_module = default_settings_module
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
        return "ZSL(application={0}, zsl_version={1}, app_version={2})".format(
            self.name, self.VERSION,
            self._app_version)

    def _configure(self, config_object=None):
        # type: (Any) -> None
        """Read the configuration from config files.
        Loads the default settings and the profile settings if available.
        Check :func:`.set_profile`.

        :param config_object:
            This parameter is the configuration decscription may be a dict or
            string describing the module from which the configuration is used.
            Default is settings.default_settings.
        """

        if config_object:
            self.config.from_mapping(config_object)
        else:
            self.config.from_object(self._default_settings_module)

        zsl_settings = os.environ.get(SETTINGS_ENV_VAR_NAME)
        if zsl_settings is not None:
            self.config.from_envvar(SETTINGS_ENV_VAR_NAME)

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
        self._register()
        self._create_injector()
        self._bind_core()
        self._bind_modules(modules)
        self.logger.debug("Injector configuration with modules {0}.".format(modules))
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

    def get_version(self):
        v = self.config.get('VERSION')
        if v is None:
            return ServiceApplication.VERSION
        else:
            return ServiceApplication.VERSION + ":" + v

    def _create_injector(self):
        self.logger.debug('Creating injector')
        self._injector = Injector()

    def _bind_core(self):
        self._injector.binder.bind(ServiceApplication, self, singleton)
        self._injector.binder.bind(Config, self.config, singleton)

    def _bind_modules(self, modules):
        for module in modules:
            self.injector.binder.install(module)

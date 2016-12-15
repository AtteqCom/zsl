from flask import Flask
import os

from zsl.interface.importer import is_initialized
from flask_injector import FlaskInjector


class AtteqServiceFlask(Flask):
    '''
    Atteq Service Flask application.
    '''

    VERSION = '1.1.4'

    def __init__(self, import_name, static_path=None, static_url_path=None,
                 static_folder='static', template_folder='templates',
                 instance_path=None, instance_relative_config=False):
        Flask.__init__(self, import_name, static_path, static_url_path,
                       static_folder, template_folder, instance_path,
                       instance_relative_config)
        self._dependencies_initialized = False
        self.config.from_object('settings.default_settings')
        asl_settings = os.environ.get('ASL_SETTINGS')
        if not asl_settings is None:
            self.config.from_envvar('ASL_SETTINGS')

    def initialize_dependencies(self, initialization_context):
        from zsl.application.initializers import injection_views, injection_modules
        self._initialization_context = initialization_context
        self._flask_injector = FlaskInjector(self, injection_views + injection_modules)
        self.set_injector(self._flask_injector.injector)
        self.logger.debug("Injector configuration {0}, {1}.".format(injection_views, injection_modules))
        self._dependencies_initialized = True

    def get_initialization_context(self):
        return self._initialization_context

    def is_initialized(self):
        return self._dependencies_initialized

    def get_injector(self):
        return self._injector

    def set_injector(self, injector):
        self._injector = injector

    def get_version(self):
        v = self.config.get('VERSION')
        if v is None:
            return AtteqServiceFlask.VERSION
        else:
            return AtteqServiceFlask.VERSION + ":" + v

if not is_initialized():
    raise Exception("Can not instantiate ServiceApplication object, the service is not initialized.")
service_application = AtteqServiceFlask("zsl.application")

from flask import Flask
import os
import asl.vendor
asl.vendor.do_init()
from flask_injector import FlaskInjector

class AtteqServiceFlask(Flask):
    def __init__(self, import_name, static_path=None, static_url_path=None,
                 static_folder='static', template_folder='templates',
                 instance_path=None, instance_relative_config=False):
        Flask.__init__(self, import_name, static_path, static_url_path,
                       static_folder, template_folder, instance_path,
                       instance_relative_config)
        self._dependencies_initialized = False
        self.config.from_object('settings.default_settings')
        asl_settings = os.environ.get('ASL_SETTINGS');
        if not asl_settings is None:
            self.config.from_envvar('ASL_SETTINGS')

    def initialize_dependencies(self):
        from asl.application.initializers import injection_views, injection_modules
        self._flask_injector = FlaskInjector(injection_views, injection_modules)
        self.set_injector(self._flask_injector.init_app(self))
        self.logger.debug("Injector configuration {0}, {1}.".format(injection_views, injection_modules))
        self._dependencies_initialized = True

    def is_initialized(self):
        return self._dependencies_initialized

    def get_injector(self):
        return self._injector

    def set_injector(self, injector):
        self._injector = injector

    def get_version(self):
        v = self.config.get('VERSION')
        if v is None:
            return '1.1'
        else:
            return '1.1' + "-" + v

service_application = AtteqServiceFlask("asl.application")

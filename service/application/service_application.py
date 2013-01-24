from flask import Flask
import os
import vendor
vendor.do_init()
from flask_injector import FlaskInjector

class SportkyFlask(Flask):
    def __init__(self, import_name, static_path=None, static_url_path=None,
                 static_folder='static', template_folder='templates',
                 instance_path=None, instance_relative_config=False):
        Flask.__init__(self, import_name, static_path, static_url_path,
                       static_folder, template_folder, instance_path,
                       instance_relative_config)
        self._dependencies_initialized = False

    def initialize_dependencies(self):
        from application.initializers import injection_views, injection_modules
        self._flask_injector = FlaskInjector(injection_views, injection_modules)
        self._injector = self._flask_injector.init_app(self)
        self.logger.debug("Injector configuration {0}, {1}.".format(injection_views, injection_modules))
        self._dependencies_initialized = True

    def is_initialized(self):
        return self._dependencies_initialized

    def get_injector(self):
        return self._injector

service_application = SportkyFlask("application")

service_application.config.from_object('settings.default_settings')
if os.environ.get('SPORTKY_SERVICE_SETTINGS', None) != None:
    service_application.config.from_envvar('SPORTKY_SERVICE_SETTINGS')

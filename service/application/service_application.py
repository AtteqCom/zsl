from flask import Flask
import os
import vendor
vendor.do_init()
from flask_injector import FlaskInjector

class SportkyFlask(Flask):
    def initialize_dependencies(self):
        from application.initializers import injection_views, injection_modules
        self.__flask_injector = FlaskInjector(injection_views, injection_modules)
        self.__injector = self.__flask_injector.init_app(self)
        self.logger.debug("Injector configuration {0}, {1}.".format(injection_views, injection_modules))

    def get_injector(self):
        return self.__injector

service_application = SportkyFlask("application")

service_application.config.from_object('settings.default_settings')
if os.environ.get('SPORTKY_SERVICE_SETTINGS', None) != None:
    service_application.config.from_envvar('SPORTKY_SERVICE_SETTINGS')

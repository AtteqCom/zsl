import vendor
from flask_injector import FlaskInjector
from application.service_application import service_application

app = service_application

injection_views = []
injection_modules = []

def injection_view():
    pass

def injection_module(f):
    injection_modules.append(f)
    return f

from .logger_initializer import LoggerInitializer

flask_injector = FlaskInjector(injection_views, injection_modules)
flask_injector.init_app(app)

import vendor

injection_views = []
injection_modules = []

def injection_view(f):
    injection_views.append(f)
    return f

def injection_module(f):
    injection_modules.append(f)
    return f

from .logger_initializer import LoggerInitializer
from .database_initializer import DatabaseInitializer
from .application_initializer import ApplicationInitializer
from .service_initializer import ServiceInitializer
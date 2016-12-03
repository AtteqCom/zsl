'''
:mod:`asl.application.initializers` -- ASL initializers
=======================================================

   :platform: Unix, Windows
   :synopsis: The Atteq Service Layer initialization infrastructure
   
.. moduleauthor:: Martin Babka <babka@atteq.com>
'''

import zsl.vendor

injection_views = []
injection_modules = []


def injection_view(f):
    '''
    Adds the view to the list of Injector-enabled views to add to the Flask app.

    :param callable f: The decorated view function. 
    '''
    injection_views.append(f)
    return f


def injection_module(f):
    '''
    Adds the module to the list of injection enabled modules. The decorated function is then called in the initialization phase and can
    create and initialize the object which will be able to be injected.

    :param callable f: The decorated initializing function.
    '''
    injection_modules.append(f)
    return f


from .logger_initializer import LoggerInitializer
from .unittest_initializer import UnitTestInitializer
from .library_initializer import LibraryInitializer
from .database_initializer import DatabaseInitializer
from .application_initializer import ApplicationInitializer
from .service_initializer import ServiceInitializer
from .cache_initializer import CacheInitializer
from .context_initializer import ContextInitializer

'''
:mod:`asl.application.initializers` -- ASL initializers
=======================================================

   :platform: Unix, Windows
   :synopsis: The Atteq Service Layer initialization infrastructure
   
.. moduleauthor:: Martin Babka <babka@atteq.com>
'''

import asl.vendor

injection_views = []
injection_modules = []

def injection_view(f):
    injection_views.append(f)
    return f

def injection_module(f):
    injection_modules.append(f)
    return f

from .logger_initializer import LoggerInitializer
from .library_initializer import LibraryInitializer
from .database_initializer import DatabaseInitializer
from .application_initializer import ApplicationInitializer
from .service_initializer import ServiceInitializer
from .cache_initializer import CacheInitializer

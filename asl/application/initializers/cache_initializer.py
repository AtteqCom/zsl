'''
Created on 24.1.2013

@author: Martin Babka
'''
import logging
from injector import singleton
from asl.application.initializers import injection_module
from werkzeug.contrib.cache import RedisCache

class CacheInitializer(object):
    '''
    Application initializer - just for the injection capability.
    '''

    def initialize(self, binder):
        '''
        Initialization method.
        '''
        binder.bind(
            RedisCache,
            to = RedisCache(),
            scope = singleton
        )
        logger = binder.injector.get(logging.Logger)
        logger.debug("Created RedisCache binding.")

@injection_module
def application_initializer_module(binder):
    CacheInitializer().initialize(binder)

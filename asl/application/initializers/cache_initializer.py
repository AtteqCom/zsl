'''
Created on 24.1.2013

@author: Martin Babka
'''
import logging
from injector import singleton
from asl.application.initializers import injection_module
from asl.cache.redis_cache_module import RedisCacheModule
from asl.cache.cache_module import CacheModule
from asl.cache.redis_id_helper import RedisIdHelper
from asl.cache.id_helper import IdHelper

class CacheInitializer(object):
    '''
    Application initializer - just for the injection capability.
    '''

    def initialize(self, binder):
        '''
        Initialization method.
        '''
        redis_cache_module = RedisCacheModule()
        binder.bind(
            RedisCacheModule,
            to = redis_cache_module,
            scope = singleton
        )
        binder.bind(
            CacheModule,
            to = redis_cache_module,
            scope = singleton
        )

        redis_id_helper = RedisIdHelper()
        binder.bind(
            RedisIdHelper,
            to = redis_id_helper,
            scope = singleton
        )
        binder.bind(
            IdHelper,
            to = redis_id_helper,
            scope = singleton
        )

        logger = binder.injector.get(logging.Logger)
        logger.debug("Created RedisCache binding.")

@injection_module
def application_initializer_module(binder):
    CacheInitializer().initialize(binder)

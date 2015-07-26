import logging
from injector import singleton
from asl.application.initializers import injection_module
from asl.cache.redis_cache_module import RedisCacheModule
from asl.cache.cache_module import CacheModule
from asl.cache.redis_id_helper import RedisIdHelper
from asl.cache.id_helper import IdHelper

class CacheInitializer(object):
    '''
    Cache initializer - adds the cache injection capability.
    '''

    def initialize(self, binder):
        '''
        Initializer of the cache - creates the Redis cache module as the default cache infrastructure. 
        The module is bound to `RedisCacheModule` and `CacheModule` keys.
        The initializer also creates `RedisIdHelper` and bounds it to `RedisIdHelper` and `IdHelper` keys.
        
        :param Binder binder: The binder object holding the binding context, we add cache to the binder.
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
    '''
    Cache initializer - adds the cache injection capability.
    
    :param Binder binder: The binder object holding the binding context, we add cache to the binder.
    '''
    CacheInitializer().initialize(binder)

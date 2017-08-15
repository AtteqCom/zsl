"""
:mod:`zsl.application.modules.cache_module`
-------------------------------------------
"""
from __future__ import unicode_literals

import logging

from injector import Binder, Module, singleton

from zsl.cache.cache_module import CacheModule
from zsl.cache.id_helper import IdHelper
from zsl.cache.redis_cache_module import RedisCacheModule
from zsl.cache.redis_id_helper import RedisIdHelper


class RedisCacheInjectionModule(Module):
    """Adds cache modules into to current configuration using reddis as
    backend.
    """

    def configure(self, binder):
        # type: (Binder) -> None
        """Initializer of the cache - creates the Redis cache module as the
        default cache infrastructure. The module is bound to `RedisCacheModule`
        and `CacheModule` keys. The initializer also creates `RedisIdHelper`
        and bounds it to `RedisIdHelper` and `IdHelper` keys.

        :param Binder binder: The binder object holding the binding context, we\
         add cache to the binder.
        """
        redis_cache_module = RedisCacheModule()
        binder.bind(
            RedisCacheModule,
            to=redis_cache_module,
            scope=singleton
        )
        binder.bind(
            CacheModule,
            to=redis_cache_module,
            scope=singleton
        )

        redis_id_helper = RedisIdHelper()
        binder.bind(
            RedisIdHelper,
            to=redis_id_helper,
            scope=singleton
        )
        binder.bind(
            IdHelper,
            to=redis_id_helper,
            scope=singleton
        )

        logging.debug("Created RedisCache binding.")

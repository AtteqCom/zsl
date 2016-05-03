'''
:mod:`asl.cache.redis_cache_module`

.. moduleauthor:: Martin Babka
'''
from asl.cache.cache_module import CacheModule
import redis
from asl.application.service_application import service_application

class RedisCacheModule(CacheModule):
    '''
    Abstraction layer for caching.
    '''
    def __init__(self):
        '''
        Abstraction layer for caching.
        '''
        self._app = service_application
        redis_conf = self._app.config['REDIS'];
        self._client = redis.StrictRedis(
            host=redis_conf['host'],
            port = redis_conf['port'],
            db = redis_conf['db'] if 'db' in redis_conf else 0,
            password = redis_conf['password'] if 'password' in redis_conf else None
        )
        self._app.logger.debug("Redis client created.")
        self._cache_prefix = service_application.config['CACHE_PREFIX'] + ':' if 'CACHE_PREFIX' in service_application.config else ''
        
    def _prefix_key(self, key):
        return self._cache_prefix + key

    def set_key(self, key, value, timeout):
        pkey = self._prefix_key(key)
        self._client.set(pkey, value)
        self.set_key_expiration(pkey, timeout)

    def invalidate_key(self, key):
        pkey = self._prefix_key(key)
        self._client.delete(pkey)

    def set_key_expiration(self, key, timeout):
        pkey = self._prefix_key(key)
        self._client.expire(pkey, timeout)
        
    def contains_key(self, key):
        pkey = self._prefix_key(key)
        return self._client.exists(pkey)

    def contains_list(self, key):
        pkey = self._prefix_key(key)
        return self._client.exists(pkey)

    def get_key(self, key):
        pkey = self._prefix_key(key)
        return self._client.get(pkey)

    def append_to_list(self, key, value):
        pkey = self._prefix_key(key)
        self._client.rpush(pkey, value)

    def get_list(self, key):
        pkey = self._prefix_key(key)
        llen = self._client.llen(pkey)
        return self._client.lrange(pkey, 0, llen - 1)

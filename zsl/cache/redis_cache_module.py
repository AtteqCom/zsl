"""
:mod:`zsl.cache.redis_cache_module`
-----------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals
from zsl.cache.cache_module import CacheModule
import redis

from zsl import inject, Zsl, Config


class RedisCacheModule(CacheModule):
    """Abstraction layer for caching."""

    @inject(app=Zsl, config=Config)
    def __init__(self, app, config):
        """Abstraction layer for caching."""
        self._app = app
        self._config = config

        redis_conf = self._config.get('REDIS', {})

        self._client = redis.StrictRedis(
            host=redis_conf.get('host'),
            port=redis_conf.get('port'),
            db=redis_conf.get('db', 0),
            password=redis_conf.get('password')
        )
        self.logger = self._app.logger.getChild('cache')
        self.logger.debug("Redis client created.")
        self._cache_prefix = self._config[
            'CACHE_PREFIX'] + ':' if 'CACHE_PREFIX' in self._config else ''

    def _prefix_key(self, key):
        return self._cache_prefix + key

    def set_key(self, key, value, timeout):
        pkey = self._prefix_key(key)
        self._client.set(pkey, value)
        self.set_key_expiration(key, timeout)

    def invalidate_key(self, key):
        pkey = self._prefix_key(key)
        self.logger.debug("Key invalidation '{0}'.".format(key))
        self._client.delete(pkey)

    def set_key_expiration(self, key, timeout):
        pkey = self._prefix_key(key)
        self.logger.debug("Key expiration '{0}' = {1}.".format(key, timeout))
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

    def invalidate_by_glob(self, glob):
        pglob = self._prefix_key(glob)

        if self._config.get('IS_USING_MEDIEVAL_SOFTWARE', False):
            keylist = self._client.keys(pglob)
        else:
            keylist = self._client.scan_iter(pglob)

        for key in keylist:
            # This does not need to prefixed.
            self.logger.debug('Invalidating key {0}.'.format(key))
            self._client.delete(key)

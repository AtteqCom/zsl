"""
:mod:`zsl.cache.redis_id_helper`
--------------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals

import logging

from zsl import Config, inject
from zsl.cache.id_helper import IdHelper, decoder_identity, encoder_identity, model_key_generator
from zsl.cache.redis_cache_module import RedisCacheModule


class RedisIdHelper(IdHelper):
    CACHE_DEFAULT_TIMEOUT = 300

    @inject(config=Config, redis_cache_module=RedisCacheModule)
    def __init__(self, config, redis_cache_module):
        """
        Creates the id helper for caching support of AppModels.
        """
        self._config = config
        self._redis_cache_module = redis_cache_module

        if 'CACHE_TIMEOUTS' in self._config:
            self._cache_timeouts = self._config['CACHE_TIMEOUTS']
        else:
            self._cache_timeouts = None
        self._cache_default_timeout = self._config.get('CACHE_DEFAULT_TIMEOUT',
                                                       RedisIdHelper.CACHE_DEFAULT_TIMEOUT)

    def get_timeout(self, key, value, timeout):
        if self._cache_timeouts is None:
            return self._cache_default_timeout
        else:
            return self._cache_timeouts[timeout]

    def gather_page(self, page_key, decoder=decoder_identity):
        page_keys = self._redis_cache_module.get_list(page_key)
        logging.debug("Fetching page {0} from redis using keys {1}.".format(page_key, page_keys))

        p = []
        for k in page_keys:
            p.append(decoder(k, self.get_key(k)))

        return p

    def fill_page(self, page_key, data, timeout, encoder=encoder_identity, model_key_generator=model_key_generator):
        self._redis_cache_module.invalidate_key(page_key)
        first = True

        for d in data:
            key = model_key_generator(d)
            self._redis_cache_module.append_to_list(page_key, key)
            if first:
                self._redis_cache_module.set_key_expiration(page_key, self.get_timeout(page_key, data, timeout))
                first = False
            self._redis_cache_module.set_key(key, encoder(d), self.get_timeout(key, d, timeout))

    def check_page(self, page_key):
        if not self._redis_cache_module.contains_list(page_key):
            return False

        page_keys = self._redis_cache_module.get_list(page_key)
        for k in page_keys:
            if not self.check_key(k):
                return False

        return True

    def check_key(self, key):
        return self._redis_cache_module.contains_key(key)

    def get_key(self, key):
        return self._redis_cache_module.get_key(key)

    def invalidate_key(self, key):
        return self._redis_cache_module.invalidate_key(key)

    def invalidate_keys_by_prefix(self, key_prefix):
        return self._redis_cache_module.invalidate_by_glob(key_prefix + "*")

    def set_key(self, key, value, timeout):
        self._redis_cache_module.set_key(key, value, self.get_timeout(key, value, timeout))

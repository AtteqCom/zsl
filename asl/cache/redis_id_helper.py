'''
Created on 12.12.2012

@author: Martin Babka
'''
from asl.cache.id_helper import IdHelper, decoder_identity, encoder_identity
from asl.utils.injection_helper import inject
from asl.cache.redis_cache_module import RedisCacheModule
from asl.utils.cache_helper import create_key_object_prefix
from asl.application.service_application import service_application

class RedisIdHelper(IdHelper):
    @inject(redis_cache_module = RedisCacheModule)
    def __init__(self, redis_cache_module):
        '''
        Creates the id helper for caching support of AppModels.
        '''
        self._redis_cache_module = redis_cache_module
        
        if 'CACHE_TIMEOUTS' in service_application.config:
            self._cache_timeouts = service_application.config['CACHE_TIMEOUTS']
        else:
            self._cache_timeouts = None

    def get_timeout(self, key, value, timeout):
        # TODO: Nejak lepsie. peto suhlasi
        if self._cache_timeouts is None:
            return 3600
        else:
            return self._cache_timeouts[timeout]

    def gather_page(self, page_key, decoder = decoder_identity):
        page_keys = self._redis_cache_module.get_list(page_key)

        p = []
        for k in page_keys:
            p.append(decoder(k, self.get_key(k)))

        return p

    def fill_page(self, page_key, data, timeout, encoder = encoder_identity):
        self._redis_cache_module.invalidate_key(page_key)

        for d in data:
            key = self.create_key(d)
            self._redis_cache_module.append_to_list(page_key, key)
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

    def set_key(self, key, value, timeout):
        self._redis_cache_module.set_key(key, value, self.get_timeout(key, value, timeout))

    def create_key(self, value):
        return "{0}-{1}".format(create_key_object_prefix(value), value.get_id())

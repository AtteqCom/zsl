'''
Created on 12.12.2012

@author: Martin Babka
'''
from asl.cache.id_helper import IdHelper
from asl.utils.injection_helper import inject
from asl.cache.redis_cache_module import RedisCacheModule

class RedisIdHelper(IdHelper):

    @inject(redis_cache_module = RedisCacheModule)
    def __init__(self, redis_cache_module):
        '''
        Creates the id helper for caching support of AppModels.
        '''
        self._redis_cache_module = redis_cache_module

    def get_timeout(self, key, value):
        # TODO: Nejak lepsie.
        return 3600

    def gather_page(self, page_key):
        page_keys = self._redis_cache_module.get_list(page_key)

        p = []
        for k in page_keys:
            p += self.get_gey(k)

    def fill_page(self, page_key, data):
        self._redis_cache_module.invalidate_key(page_key)

        for d in data:
            key = self.create_key(d)
            self._redis_cache_module.append_to_list(page_key, key)
            self._redis_cache_module.set_key(key, d)

    def check_key(self, key):
        return self._redis_cache_client.contains_key()

    def check_page(self, page_key):
        page_keys = self._redis_cache_client.get_list(page_key)
        if page_keys == None:
            return False

        for k in page_keys:
            if not self.check_key(k):
                return False

        return True

    def save(self, key, value):
        self._redis_cache_client.save_key(key, value, self.get_timeout(key, value))

    def create_key(self, value):
        return "{0}.{1}-{2}".format(value.__class__.__module__, value.__class__.name, value.get_id())

    def create_page_key(self, value, page_no):
        return "{0}.{1}-page-{2}".format(value.__class__.__module__, value.__class__.name, page_no)

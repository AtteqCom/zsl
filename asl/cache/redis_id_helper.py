'''
Created on 12.12.2012

@author: Martin Babka
'''
from asl.cache.id_helper import IdHelper

class RedisIdHelper(IdHelper):
    def __init__(self, redis_cache_client):
        pass

    def gather_page(self, key, page_no):
        pass

    def fill_page(self, key, page_no, data):
        pass

    def check_key(self, key):
        pass

    def check_page(self, key, page_no):
        pass

    def save(self, key, value):
        pass

    def create_key(self, value):
        pass

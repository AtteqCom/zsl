import redis
from asl.application import service_application

'''
Created on 22.1.2013

@author: Martin Babka
'''

class RedisCacheClient(object):
    '''
    Abstraction layer for caching.
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

        self._app = service_application
        redis_conf = self._app.config['REDIS'];
        self._client = redis.StrictRedis(host=redis_conf['host'], port = redis_conf['port'], db = redis_conf['db'])
        self._app.logger.debug("Redis client created.")

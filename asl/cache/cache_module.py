'''
Created on 6.4.2013

@author: Martin Babka
'''

import abc

class CacheModule(object):
    '''
    Cache abstraction layer - module for caching.
    '''

    @abc.abstractmethod
    def set_key(self, key, value, timeout):
        '''
        Saves the ``key``-``value`` pair for ``timeout`` seconds.
        '''
        pass

    @abc.abstractmethod
    def invalidate_key(self, key):
        '''
        Deletes the ``key``.
        '''
        pass

    @abc.abstractmethod
    def contains_key(self, key):
        '''
        Check if the ``key`` is contained in the cache.
        '''
        pass

    @abc.abstractmethod
    def get_key(self, key):
        '''
        Returns the value associated with the ``key``.
        '''
        pass

    @abc.abstractmethod
    def get_list(self, key):
        '''
        Returns the list associated with the ``key``.
        '''
        pass

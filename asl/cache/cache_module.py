'''
:mod:`asl.cache.cache_module`

.. moduleauthor:: Martin Babka
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
        
        TODO morihladko sa pyta: nemalo by sa skor volat get_by_key, ci simple get(self, key), lebo get_key mi asociujuje ze to vrati kluc
        '''
        pass

    @abc.abstractmethod
    def contains_list(self, key):
        '''
        Check if the ``key`` is in the cache.
        '''
        pass

    @abc.abstractmethod
    def get_list(self, key):
        '''
        Returns the list associated with the ``key``.
        '''
        pass

    @abc.abstractmethod
    def invalidate_by_glob(self, glob):
        '''
        Invalidates the keys by given glob.
        
        :param string glob: All the keys matching the given glob will be invalidated.
        '''

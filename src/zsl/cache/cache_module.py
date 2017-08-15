"""
:mod:`zsl.cache.cache_module`
-----------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

import abc
from builtins import object

from future.utils import with_metaclass


class CacheModule(with_metaclass(abc.ABCMeta, object)):
    """
    Cache abstraction layer - module for caching.
    """

    @abc.abstractmethod
    def set_key(self, key, value, timeout):
        """
        Saves the ``key``-``value`` pair for ``timeout`` seconds.
        """
        pass

    @abc.abstractmethod
    def invalidate_key(self, key):
        """
        Deletes the ``key``.
        """
        pass

    @abc.abstractmethod
    def contains_key(self, key):
        """
        Check if the ``key`` is contained in the cache.
        """
        pass

    @abc.abstractmethod
    def get_key(self, key):
        """
        Returns the value associated with the ``key``.

        TODO this should be named get_by_key or just simply get(key), get_key sounds like it would return a key
        """
        pass

    @abc.abstractmethod
    def contains_list(self, key):
        """
        Check if the ``key`` is in the cache.
        """
        pass

    @abc.abstractmethod
    def get_list(self, key):
        """
        Returns the list associated with the ``key``.
        """
        pass

    @abc.abstractmethod
    def invalidate_by_glob(self, glob):
        """
        Invalidates the keys by given glob.

        :param string glob: All the keys matching the given glob will be invalidated.
        """

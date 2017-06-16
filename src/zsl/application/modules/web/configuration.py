from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from zsl.configuration import InvalidConfigurationException


class MethodConfiguration(object):
    def __init__(self, package=None, packages=None, url_prefix='method'):
        if packages is not None and package is not None:
            raise InvalidConfigurationException("Can not take both packages and package in method configuration.")
        packages = tuple(packages) if packages is not None else ()
        self._packages = (package,) if package is not None else packages

        if '/' in url_prefix:
            raise InvalidConfigurationException("MethodConfiguration url_prefix parameter can not contain slashes.")
        self._url_prefix = url_prefix

    @property
    def url_prefix(self):
        return self._url_prefix

    @property
    def packages(self):
        return self._packages

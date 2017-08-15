"""
:mod:`zsl.interface.webservice.performers.method`
-------------------------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

from importlib import import_module
import logging
import sys

from zsl.router.method import get_method_packages


def call_exposers_in_method_packages():
    for package in get_method_packages():
        if package in sys.modules:
            module = sys.modules[package]
            if hasattr(module, '__reloader__'):
                getattr(module, '__reloader__')()
        else:
            module = import_module(package)

        msg = "Calling exposers in method package {}".format(package)
        logging.getLogger(__name__).debug(msg)
        if hasattr(module, '__exposer__'):
            getattr(module, '__exposer__')()

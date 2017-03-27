"""
:mod:`zsl.interface.webservice.performers.method`
-------------------------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals
from zsl.router.method import get_method_packages
import importlib


def call_exposers_in_method_packages():
    for package in get_method_packages():
        module = importlib.import_module(package)
        if hasattr(module, '__exposer__'):
            getattr(module, '__exposer__')()

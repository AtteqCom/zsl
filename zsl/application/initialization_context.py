"""
:mod:`zsl.application.initialization_context`
---------------------------------------------

The modules deals with the initialization of the basics - python path and then
loads and initializes the application if necessary.

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals


class InitializationContext(object):
    def __init__(self, unit_test=False, initializers=None):
        if not initializers:
            initializers = []

        self._unit_test = unit_test
        self._initializers = initializers
        self._is_initialized = False

    def get_unit_testing(self):
        return self._unit_test

    unit_testing = property(get_unit_testing)

    @property
    def is_initialized(self):
        return self._is_initialized

    def initialize(self):
        for i in self._initializers:
            i.initialize()

        self._is_initialized = True

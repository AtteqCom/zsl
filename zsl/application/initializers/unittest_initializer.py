"""
:mod:`zsl.application.initializers.unittest_initializer`
--------------------------------------------------------
"""
from __future__ import unicode_literals
from builtins import object
from zsl.application.initializers import injection_module
from zsl.application.service_application import service_application


class UnitTestInitializer(object):
    """
    Initializer handling the unit test settings.
    """

    def initialize(self, binder):

        if not self.is_unit_testing():
            return

        if 'TEST_DATABASE_URI' in service_application.config:
            service_application.config['DATABASE_URI'] = service_application.config['TEST_DATABASE_URI']

        if 'TEST_DATABASE_ENGINE_PROPS' in service_application.config:
            service_application.config['DATABASE_ENGINE_PROPS'] = service_application.config[
                'TEST_DATABASE_ENGINE_PROPS']

    @staticmethod
    def is_unit_testing():
        return service_application.get_initialization_context().unit_testing


@injection_module
def application_initializer_module(binder):
    UnitTestInitializer().initialize(binder)

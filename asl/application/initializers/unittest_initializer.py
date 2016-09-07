from asl.application.initializers import injection_module
from asl.application.service_application import service_application


class UnitTestInitializer(object):
    '''
    Initializer handling the unit test settings.
    '''

    def initialize(self, binder):

        if not self.is_unit_testing():
            return

        service_application.config['DATABASE_URI'] = service_application.config['TEST_DATABASE_URI']
        service_application.config['DATABASE_ENGINE_PROPS'] = service_application.config['TEST_DATABASE_ENGINE_PROPS']

    def is_unit_testing(self):
        return service_application.get_initialization_context().unit_testing


@injection_module
def application_initializer_module(binder):
    UnitTestInitializer().initialize(binder)

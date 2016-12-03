from injector import singleton
import logging
from zsl.application.service_application import service_application
import importlib
from zsl.application.initializers import injection_module


class ContextInitializer(object):
    '''
    Initializer handling the service injection.
    '''

    def bind(self, cls, instance):
        self._binder.bind(
            cls,
            to=instance,
            scope=singleton
        )
        logger = self._binder.injector.get(logging.Logger)
        logger.debug("Created {0} binding.".format(cls))

    def initialize(self, binder):
        '''
        Initialization method.
        '''
        context_injection_config = service_application.config.get('CONTEXT_INJECTION')
        if not context_injection_config:
            return

        m = importlib.import_module(context_injection_config)
        self._binder = binder
        getattr(m, 'initialize_context')(self)


@injection_module
def application_initializer_module(binder):
    ContextInitializer().initialize(binder)

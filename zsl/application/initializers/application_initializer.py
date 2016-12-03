import logging
from zsl.application.service_application import service_application, AtteqServiceFlask
from flask.config import Config
from injector import singleton
from zsl.application.initializers import injection_module


class ApplicationInitializer(object):
    """
    :class:`zsl.application.initializers.ApplicationInitializer` adds the injection capability of the application object.
    The application object is bound as `AtteqServiceFlask`.
    """

    def initialize(self, binder):
        '''
        Initialization method which bounds the application object to `AtteqServiceFlask` key.
        '''
        # Bind app
        binder.bind(
            AtteqServiceFlask,
            to=service_application,
            scope=singleton
        )

        service_application.set_injector(binder.injector)
        logger = binder.injector.get(logging.Logger)
        logger.debug("Created AtteqServiceFlask binding.")

        # Bind the Config
        binder.bind(
            Config,
            to=service_application.config,
            scope=singleton
        )
        logger.debug("Created Config binding.")


@injection_module
def application_initializer_module(binder):
    '''
    Application initializer - just for the injection capability of the application object.

    See :class:`zsl.application.initializers.ApplicationInitializer`.
    '''
    ApplicationInitializer().initialize(binder)

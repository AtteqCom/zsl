'''
:mod:`asl.application.initializers.logger_initializer` -- Initialization of the logger.

   :platform: Unix, Windows
   :synopsis: The Atteq Service Layer
.. moduleauthor:: Martin Babka <babka@atteq.com>
'''

from asl.application.service_application import service_application
from flask import Config
import logging
import asl.vendor
from logging import Formatter
from logging.handlers import SysLogHandler
asl.vendor.do_init()
from injector import singleton
from asl.application.initializers import injection_module

app = service_application

class LoggerInitializer:

    def _create_handler(self, handler_settings):
        parameters = handler_settings['parameters'] if 'parameters' in handler_settings else {}
        handler_type = handler_settings['type']

        if handler_type == "syslog":
            handler = SysLogHandler(**parameters)
        elif handler_type == "file":
            handler = logging.FileHandler(**parameters)
        elif handler_type == "rotating-file":
            handler = logging.handlers.RotatingFileHandler(**parameters)
        elif getattr(logging, handler_type):
            handler = getattr(logging, handler_type)(**parameters)
        else:
            raise Exception('Unknown logger type {0}.'.fromat(handler_settings['type']))

        handler.setFormatter(Formatter('[%(asctime)s %(name)s %(filename)s:%(levelname)s] %(message)s'))
        return handler

    def _check_deprecated_config_properties(self, config):
        deprecated_properties = ['LOG_HANDLER', 'LOG_LEVEL', 'SYSLOG_PARAMS', 'DATABASE_LOG_LEVEL']
        log = logging.getLogger(app.logger_name)

        for prop in deprecated_properties:
            if prop in config:
                log.warn("Config property {0} is deprecated and is ignored. Use the new logging setting.".format(prop))

    def initialize(self, binder):
        config = binder.injector.get(Config)
        binder.bind(
            logging.Logger,
            to=app.logger,
            scope=singleton
        )

        errors = []

        # Create the handlers.
        handlers = {}
        for (handler_name, handler_settings) in config.get('LOG_HANDLERS', {}).iteritems():
            try:
                handlers[handler_name] = self._create_handler(handler_settings)
            except Exception as e:
                errors.append(e)

        # Set up the loggers.
        for (logger_name, logger_settings) in config.get('LOG', {}).iteritems():
            logger = logging.getLogger(logger_name)
            logger.setLevel(getattr(logging, logger_settings['level']))
            for handler_name in logger_settings['handlers']:
                try:
                    logger.addHandler(handlers[handler_name])
                except Exception as e:
                    errors.append(e)

            logger.propagate = logger_settings.get('propagate', logger.propagate)

        self._check_deprecated_config_properties(config)
        for e in errors:
            app.logger.error(e)

@injection_module
def logger_initializer_module(binder):
    LoggerInitializer().initialize(binder)

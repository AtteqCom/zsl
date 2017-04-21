"""
:mod:`zsl.application.modules.logger_module`
--------------------------------------------
"""
from __future__ import unicode_literals
from future.utils import viewitems

import logging
from logging import Formatter
from logging.handlers import SysLogHandler

from injector import Binder, Module, provides, inject, singleton

from zsl import Zsl, Config
from zsl.utils.import_helper import fetch_class


def _create_handler(handler_settings):
    parameters = handler_settings['parameters'] if 'parameters' in handler_settings else {}
    handler_type = handler_settings['type']

    if handler_type == "syslog":
        handler = SysLogHandler(**parameters)
    elif handler_type == "file":
        handler = logging.FileHandler(**parameters)
    elif handler_type == "rotating-file":
        handler = logging.handlers.RotatingFileHandler(**parameters)
    elif hasattr(logging, handler_type):
        handler = getattr(logging, handler_type)(**parameters)
    else:
        try:
            handler = fetch_class(handler_type)(**parameters)
        except:
            raise Exception('Unknown logger type {0}.'.fromat(handler_settings['type']))

    if 'level' in handler_settings:
        handler.setLevel(handler_settings['level'])

    handler.setFormatter(Formatter('[%(asctime)s %(name)s %(filename)s:%(levelname)s] %(message)s'))
    return handler


def _check_deprecated_config_properties(config):
    deprecated_properties = ['LOG_HANDLER', 'LOG_LEVEL', 'SYSLOG_PARAMS', 'DATABASE_LOG_LEVEL']
    log = logging.getLogger(app.logger_name)

    for prop in deprecated_properties:
        if prop in config:
            log.warn("Config property {0} is deprecated and is ignored. Use the new logging setting.".format(prop))


class LoggerModule(Module):
    """Configure the application logger."""
    @provides(logging.Logger, scope=singleton)
    @inject(config=Config, app=Zsl)
    def provide_logger(self, config, app):
        # type: (Binder) -> None

        errors = []

        # Create the handlers.
        handlers = {}
        for handler_name, handler_settings in viewitems(config.get('LOG_HANDLERS', {})):
            try:
                handlers[handler_name] = self._create_handler(handler_settings)
            except Exception as e:
                errors.append(e)

        # Set up the loggers.
        for logger_name, logger_settings in viewitems(config.get('LOG', {})):
            logger = logging.getLogger(logger_name)
            logger.setLevel(getattr(logging, logger_settings['level']))
            for handler_name in logger_settings.get('handlers', []):
                try:
                    logger.addHandler(handlers[handler_name])
                except Exception as e:
                    errors.append(e)

            logger.propagate = logger_settings.get('propagate', logger.propagate)

        self._check_deprecated_config_properties(config)
        for e in errors:
            app.logger.error(e)

        return app.logger

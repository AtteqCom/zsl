"""
:mod:`zsl.application.modules.logger_module`
--------------------------------------------
"""
from __future__ import unicode_literals

import logging.config

from injector import Binder, Module

from zsl import Config, Zsl, inject


class LoggerModule(Module):
    """Configure the application logger."""

    LOGGING_CONFIG_NAME = 'LOGGING'

    def configure(self, binder):
        # type: (Binder) -> None
        super(LoggerModule, self).configure(binder)
        self.configure_logging()

    @inject(config=Config, app=Zsl)
    def configure_logging(self, config, app):
        # type: (Config) -> None
        default_config = dict(
            version=1,
            root=dict(
                level='DEBUG' if config.get('DEBUG', False) else 'WARNING'
            )
        )
        logging.config.dictConfig(config.get(LoggerModule.LOGGING_CONFIG_NAME, default_config))
        self._recreate_app_logger(app)

    def _recreate_app_logger(self, app):
        logging._acquireLock()
        del logging.getLogger(app.logger_name).manager.loggerDict[app.logger_name]
        logging._releaseLock()
        app._logger = logging.getLogger(app.logger_name)

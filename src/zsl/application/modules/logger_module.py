"""
:mod:`zsl.application.modules.logger_module`
--------------------------------------------
"""
import logging.config

from injector import Binder, Module, inject

from zsl import Config, Zsl


class LoggerModule(Module):
    """Configure the application logger."""

    LOGGING_CONFIG_NAME = 'LOGGING'

    def configure(self, binder: Binder) -> None:
        super(LoggerModule, self).configure(binder)
        binder.injector.call_with_injection(self.configure_logging)

    @inject
    def configure_logging(self, config: Config, app: Zsl) -> None:
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
        del logging.getLogger(app.name).manager.loggerDict[app.name]
        logging._releaseLock()
        app._logger = logging.getLogger(app.name)

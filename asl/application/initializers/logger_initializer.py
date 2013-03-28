from asl.application.service_application import service_application
from flask import Config
import logging
import asl.vendor
asl.vendor.do_init()
from injector import singleton
from asl.application.initializers import injection_module

app = service_application

class LoggerInitializer:

    def initialize(self, binder):
        config = binder.injector.get(Config)
        binder.bind(
            logging.Logger,
            to=app.logger,
            scope=singleton
        )

        file_handler = logging.FileHandler(config['LOG_FILE'])
        file_handler.setLevel(config['LOG_LEVEL'])
        app.logger.addHandler(file_handler)

        db_logger = logging.getLogger('sqlalchemy.engine')
        db_logger.setLevel(config['DATABASE_LOG_LEVEL'])
        db_logger.addHandler(file_handler)

@injection_module
def logger_initializer_module(binder):
    LoggerInitializer().initialize(binder)

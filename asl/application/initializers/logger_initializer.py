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

    def initialize(self, binder):
        config = binder.injector.get(Config)
        binder.bind(
            logging.Logger,
            to=app.logger,
            scope=singleton
        )

        if 'LOG_HANDLER' not in config:
            config['LOG_HANDLER'] = 'rotating-file'
        if 'LOG_LEVEL' not in config:
            config['LOG_LEVEL'] = 'DEBUG' if app.debug else 'WARNING'
        else:
            config['LOG_LEVEL'] = config['LOG_LEVEL']

        if config['LOG_HANDLER'] == "syslog":
            handler = SysLogHandler(**config['SYSLOG_PARAMS'])
        elif config['LOG_HANDLER'] == "file":
            handler = logging.FileHandler(config['LOG_FILE'])
        elif config['LOG_HANDLER'] == "rotating-file":
            handler = logging.handlers.RotatingFileHandler(config['LOG_FILE'])
        elif config['LOG_HANDLER'] == None or config['LOG_HANDLER'].lower() == 'none':
            return

        handler.setLevel(getattr(logging, config['LOG_LEVEL']))
        handler.setFormatter(Formatter('[%(asctime)s] [%(name)s-%(levelname)s] [%(filename)s] %(message)s'))

        logging.getLogger(app.logger_name).addHandler(handler)
        logging.getLogger(app.logger_name).setLevel(getattr(logging, config['LOG_LEVEL']))

        db_logger = logging.getLogger('sqlalchemy.engine')
        db_logger.setLevel(config['DATABASE_LOG_LEVEL'])
        db_logger.addHandler(handler)

@injection_module
def logger_initializer_module(binder):
    LoggerInitializer().initialize(binder)

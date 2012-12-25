from flask import Config
import vendor
import logging
import sqlalchemy
vendor.do_init()
from injector import singleton
from application.initializers import injection_module

class DatabaseInitializer:
    def initialize(self, binder):
        config = binder.injector.get(Config)
        binder.bind(
            sqlalchemy.engine.Engine,
            to=sqlalchemy.create_engine(config['DATABASE_URI']),
            scope=singleton
        )
        logger = binder.injector.get(logging.Logger)
        logger.debug("Created DB configuration to {0}.".format(config['DATABASE_URI']))

@injection_module
def database_initializer_module(binder):
    DatabaseInitializer().initialize(binder)

from flask import Config
import vendor
import logging
from sqlalchemy import create_engine
import sqlalchemy.orm
import sqlalchemy.engine
vendor.do_init()
from injector import singleton
from application.initializers import injection_module

class DatabaseInitializer:
    def initialize(self, binder):
        config = binder.injector.get(Config)
        engine = create_engine(config['DATABASE_URI'])

        binder.bind(
            sqlalchemy.engine.Engine,
            to = engine,
            scope = singleton
        )
        logger = binder.injector.get(logging.Logger)
        logger.debug("Created DB configuration to {0}.".format(config['DATABASE_URI']))

        binder.bind(
            sqlalchemy.orm.Session,
            to = sqlalchemy.orm.sessionmaker(engine),
            scope = singleton
        )
        logger.debug("Created ORM session")

@injection_module
def database_initializer_module(binder):
    DatabaseInitializer().initialize(binder)

from flask import Config
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.engine.base import Engine
from injector import singleton
from zsl.application.initializers import injection_module


class SessionHolder:

    def __init__(self, sess_cls):
        self._sess_cls = sess_cls

    def __call__(self):
        return self._sess_cls()


class DatabaseInitializer:

    def initialize(self, binder):
        config = binder.injector.get(Config)
        engine = create_engine(config['DATABASE_URI'], **config['DATABASE_ENGINE_PROPS'])

        binder.bind(
            Engine,
            to=engine,
            scope=singleton
        )
        logger = binder.injector.get(logging.Logger)
        logger.debug("Created DB configuration to {0}.".format(config['DATABASE_URI']))

        session = SessionHolder(sessionmaker(engine, autocommit=False, expire_on_commit=False))
        binder.bind(
            SessionHolder,
            to=session,
            scope=singleton
        )
        logger.debug("Created ORM session")


@injection_module
def database_initializer_module(binder):
    DatabaseInitializer().initialize(binder)

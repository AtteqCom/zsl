"""
:mod:`zsl.application.modules.alchemy_module`
---------------------------------------------
"""
from __future__ import unicode_literals
from builtins import object

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker, Session
from sqlalchemy.engine.base import Engine

from injector import Module, provides, singleton, inject

from zsl import Config


class SessionHolder(object):
    def __init__(self, sess_cls):
        self._sess_cls = sess_cls

    def __call__(self):
        # type: () -> Session
        return self._sess_cls()


class AlchemyModule(Module):
    """Adds SQLAlchemy to current configuration."""
    @provides(Engine, scope=singleton)
    @inject(config=Config)
    def provide_engine(self, config):
        # type: (Config) -> Engine

        engine = create_engine(config['DATABASE_URI'], **config['DATABASE_ENGINE_PROPS'])
        logging.debug("Created DB configuration to {0}.".format(config['DATABASE_URI']))

        return engine

    @provides(SessionHolder, scope=singleton)
    @inject(engine=Engine)
    def provide_session_holder(self, engine):
        # type: (Engine) -> SessionHolder

        session = SessionHolder(sessionmaker(engine, autocommit=False, expire_on_commit=False))
        logging.debug("Created ORM session")

        return session

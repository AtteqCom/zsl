"""
:mod:`zsl.application.modules.alchemy_module`
---------------------------------------------
"""
from abc import ABCMeta, abstractmethod
import logging

from injector import Module, provides, singleton
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session, sessionmaker

from zsl import Config, inject

logger = logging.getLogger(__name__)


class SessionHolder:
    def __init__(self, sess_cls):
        self._sess_cls = sess_cls

    def __call__(self) -> Session:
        return self._sess_cls()


class SessionFactory:
    """Creates a db session with an open transaction."""

    @inject(session_holder=SessionHolder)
    def __init__(self, session_holder: SessionHolder) -> None:
        self._session_holder = session_holder

    def create_session(self) -> Session:
        return self._session_holder()


class TransactionHolder:
    """
    Holds the transaction and session.

    Works like a SQAlchemy session proxy.
    """

    def __init__(self):
        self._orm = None
        self._transaction_callback = []
        self._in_transaction = False

    def has_session(self) -> bool:
        return self._orm is not None

    @property
    def session(self) -> Session:
        return self._orm

    @property
    def in_transaction(self):
        return self._in_transaction

    def inject_session(self, session: Session) -> None:
        """Used to set the session in the @transactional decorator."""
        self._orm = session
        self._in_transaction = True

    def begin(self):
        pass

    def commit(self):
        logger.debug("Commit.")
        self._orm.commit()

    def rollback(self):
        logger.debug("Rollback.")
        self._orm.rollback()

    def close(self):
        logger.debug("Close.")
        self._orm.close()
        self._orm = None
        self._in_transaction = False

    def append_transaction_callback(self, callback):
        self._transaction_callback.append(callback)

    def run_transaction_callbacks(self):
        callbacks = self._transaction_callback
        self._transaction_callback = []
        for c in callbacks:
            c()


class EmptyTransactionalHolder:
    def __init__(self):
        self._session = None

    @property
    def session(self):
        return self._session


class TransactionHolderFactory:
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_transaction_holder(self) -> TransactionHolder:
        pass


class DefaultTransactionHolderFactory(TransactionHolderFactory):
    def create_transaction_holder(self) -> TransactionHolder:
        return TransactionHolder()


class AlchemyModule(Module):
    """Adds SQLAlchemy to current configuration."""

    @provides(Engine, scope=singleton)
    @inject(config=Config)
    def provide_engine(self, config: Config) -> Engine:
        engine = create_engine(
            config["DATABASE_URI"], **config["DATABASE_ENGINE_PROPS"]
        )
        logging.debug("Created DB configuration to {0}.".format(config["DATABASE_URI"]))

        return engine

    @provides(SessionHolder, scope=singleton)
    @inject(engine=Engine)
    def provide_session_holder(self, engine: Engine) -> SessionHolder:
        session = SessionHolder(
            sessionmaker(engine, autocommit=False, expire_on_commit=False)
        )
        logging.debug("Created ORM session")

        return session

    @provides(TransactionHolderFactory, scope=singleton)
    def provide_transaction_holder_factory(self) -> TransactionHolderFactory:
        return DefaultTransactionHolderFactory()

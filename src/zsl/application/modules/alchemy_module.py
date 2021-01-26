"""
:mod:`zsl.application.modules.alchemy_module`
---------------------------------------------
"""
from abc import ABC, abstractmethod
import logging
from typing import Callable, Type

from injector import Module, inject, provider, singleton
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session, sessionmaker

from zsl import Config


class SessionHolder:
    def __init__(self, sess_cls: Type[Session]) -> None:
        self._sess_cls = sess_cls

    def __call__(self) -> Session:
        return self._sess_cls()


class SessionFactory:
    """Creates a db session with an open transaction."""

    @inject
    def __init__(self, session_holder: SessionHolder) -> None:
        self._session_holder = session_holder

    def create_session(self) -> Session:
        return self._session_holder()


class TransactionHolder:
    def __init__(self) -> None:
        self._orm = None
        self._transaction_callback = []
        self._in_transaction = False

    def has_session(self) -> bool:
        return self._orm is not None

    @property
    def session(self) -> Session:
        return self._orm

    @property
    def in_transaction(self) -> bool:
        return self._in_transaction

    def inject_session(self, session: Session) -> None:
        """Used to set the session in the @transactional decorator."""
        self._orm = session
        self._in_transaction = True

    def begin(self) -> None:
        pass

    def commit(self) -> None:
        logging.getLogger(__name__).debug("Commit.")
        self._orm.commit()

    def rollback(self) -> None:
        logging.getLogger(__name__).debug("Rollback.")
        self._orm.rollback()

    def close(self) -> None:
        logging.getLogger(__name__).debug("Close.")
        self._orm.close()
        self._orm = None
        self._in_transaction = False

    def append_transaction_callback(self, callback: Callable[[], None]) -> None:
        self._transaction_callback.append(callback)

    def run_transaction_callbacks(self) -> None:
        callbacks = self._transaction_callback
        self._transaction_callback = []
        for c in callbacks:
            c()


class EmptyTransactionalHolder:
    def __init__(self) -> None:
        self._session = None

    @property
    def session(self) -> Session:
        return self._session


class TransactionHolderFactory(ABC):

    @abstractmethod
    def create_transaction_holder(self) -> TransactionHolder:
        raise NotImplementedError()


class DefaultTransactionHolderFactory(TransactionHolderFactory):
    def create_transaction_holder(self) -> TransactionHolder:
        return TransactionHolder()


class AlchemyModule(Module):
    """Adds SQLAlchemy to current configuration."""

    @singleton
    @provider
    @inject
    def provide_engine(self, config: Config) -> Engine:
        engine = create_engine(config['DATABASE_URI'],
                               **config['DATABASE_ENGINE_PROPS'])
        logging.debug("Created DB configuration to {0}.".
                      format(config['DATABASE_URI']))

        return engine

    @singleton
    @provider
    @inject
    def provide_session_holder(self, engine: Engine) -> SessionHolder:
        session = SessionHolder(sessionmaker(engine, autocommit=False,
                                             expire_on_commit=False))
        logging.debug("Created ORM session")

        return session

    @singleton
    @provider
    def provide_transaction_holder_factory(self) -> TransactionHolderFactory:
        return DefaultTransactionHolderFactory()

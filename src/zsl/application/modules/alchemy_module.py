"""
:mod:`zsl.application.modules.alchemy_module`
---------------------------------------------
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
import logging
from threading import current_thread
from typing import Any

from injector import Module, provides, singleton
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session, sessionmaker

from zsl import Config, inject
from zsl.task.job_context import JobContext

logger = logging.getLogger(__name__)


class EnginePool:
    _DEFAULT_ENGINE_NAME = "default"

    def __init__(self, config: Config) -> None:
        self._engines: dict[str, Engine] = {}

        self._engines[self._DEFAULT_ENGINE_NAME] = create_engine(
            config["DATABASE_URI"], **config["DATABASE_ENGINE_PROPS"]
        )
        logging.debug("Created default (slave) engine")

        if config.get("DATABASE_MASTER_NODE_NAME") is not None:
            self._engines[config["DATABASE_MASTER_NODE_NAME"]] = create_engine(
                config["DATABASE_URI"],
                connect_args={"application_name": config["DATABASE_MASTER_NODE_NAME"]},
                **config["DATABASE_ENGINE_PROPS"],
            )
            logging.debug("Created master engine")

    def get_engine(self, node_name: str) -> Engine:
        return self._engines[node_name]


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


class DbNodeContext:
    """
    Context for transactional operations.

    This class is used to store the transactional context for the current thread.
    """

    def __init__(self, node_name: str | None):
        self._node_name = node_name

    @property
    def node_name(self) -> str | None:
        return self._node_name

    @classmethod
    def try_getting_current_context(cls) -> DbNodeContext | None:
        """
        Try to get the current context.

        :return: Current context.
        """
        return getattr(current_thread(), "_db_node_context", None)

    @classmethod
    def set_current_context(cls, context: "DbNodeContext") -> None:
        current_thread()._db_node_context = context


class RoutingSession(Session):

    def __init__(
        self, config: Config, engine_pool: EnginePool, *args: Any, **kwargs: Any
    ):
        self._engine_pool = engine_pool
        self._config = config
        super().__init__(*args, **kwargs)

    def get_bind(self, mapper=None, clause=None, **kwargs):
        """
        Routes to appropriate engine based on the current context.
        """

        node_name = self._get_db_node()
        return self._engine_pool.get_engine(node_name)

    def _get_db_node(self) -> str:
        db_node_context = DbNodeContext.try_getting_current_context()
        if db_node_context is not None and db_node_context.node_name is not None:
            return db_node_context.node_name

        master_node_name = self._config.get("DATABASE_MASTER_NODE_NAME")
        if master_node_name is None:
            return EnginePool._DEFAULT_ENGINE_NAME

        try:
            job_context = JobContext.get_current_context()
            return (
                master_node_name
                if job_context.task_use_master_node
                else EnginePool._DEFAULT_ENGINE_NAME
            )
        except AttributeError:
            return EnginePool._DEFAULT_ENGINE_NAME


class AlchemyModule(Module):
    """Adds SQLAlchemy to current configuration."""

    @provides(EnginePool, scope=singleton)
    @inject(config=Config)
    def provide_engine_pool(self, config: Config) -> EnginePool:
        return EnginePool(config)

    @provides(SessionHolder, scope=singleton)
    @inject(engine=EnginePool, config=Config)
    def provide_session_holder(self, engine: Engine, config: Config) -> SessionHolder:
        SessionFactory = sessionmaker(
            class_=RoutingSession,
            autocommit=False,
            expire_on_commit=False,
        )
        session_holder = SessionHolder(
            lambda: SessionFactory(engine_pool=engine, config=config)
        )
        logging.debug("Created ORM session")

        return session_holder

    @provides(TransactionHolderFactory, scope=singleton)
    def provide_transaction_holder_factory(self) -> TransactionHolderFactory:
        return DefaultTransactionHolderFactory()

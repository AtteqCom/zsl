"""
:mod:`zsl.service.service`
--------------------------

.. moduleauthor:: Martin Babka <babka@atteq.com>,
                  Peter Morihladko <morihladko@atteq.com>
"""

from __future__ import annotations

from contextlib import contextmanager
from functools import wraps
import logging
from typing import Callable, Generator

from sqlalchemy.orm.session import Session

from zsl import Config, Injected, Zsl, inject
from zsl.application.modules.alchemy_module import (DbNodeContext, EmptyTransactionalHolder, SessionFactory,
                                                    TransactionHolderFactory)

_EMPTY_TX_HOLDER = EmptyTransactionalHolder()

logger = logging.getLogger(__name__)


class TransactionalSupportMixin:
    """This mixin allows the objects to access transactional holder."""

    @property
    def _orm(self) -> Session:
        return getattr(self, _TX_HOLDER_ATTRIBUTE, _EMPTY_TX_HOLDER).session


class Service(TransactionalSupportMixin):
    """
    Main service class.
    """

    @inject(app=Zsl)
    def __init__(self, app=Injected, engine=Injected):
        """Constructor - initializes and injects the needed libraries."""
        super().__init__()
        self._app = app


_TX_HOLDER_ATTRIBUTE = "_tx_holder"


@inject(session_factory=SessionFactory)
def _get_session_factory(session_factory: SessionFactory = Injected) -> SessionFactory:
    return session_factory


@inject(tx_holder_factory=TransactionHolderFactory)
def _get_tx_holder_factory(
    tx_holder_factory: TransactionHolderFactory = Injected,
) -> TransactionHolderFactory:
    return tx_holder_factory


@contextmanager
def tx_session(service: TransactionalSupportMixin) -> Generator[Session, None, None]:
    """
    Context manager for transactional session.

    :param service: Service instance.
    :return: Session.

    .. code-block:: python

        from zsl.service import tx_session

        class MyService(Service):
            def my_method(self):
                with tx_session(self) as session:
                    self._repository.create(session, 2, 3, 4)

    """
    session_factory = _get_session_factory()
    transaction_is_open = False

    assert isinstance(service, TransactionalSupportMixin)

    if hasattr(service, _TX_HOLDER_ATTRIBUTE):
        tx_holder = getattr(service, _TX_HOLDER_ATTRIBUTE)
        assert tx_holder.has_session()
    else:
        tx_holder = _get_tx_holder_factory().create_transaction_holder()
        setattr(service, _TX_HOLDER_ATTRIBUTE, tx_holder)
        transaction_is_open = True

    try:
        logger.debug("Entering transactional method.")
        if not tx_holder.has_session():
            session = session_factory.create_session()
            tx_holder.inject_session(session)

        tx_holder.begin()

        yield tx_holder.session

        if transaction_is_open:
            tx_holder.run_transaction_callbacks()
            tx_holder.commit()

    except Exception:
        if transaction_is_open:
            tx_holder.rollback()
        raise
    finally:
        logger.debug("Finishing transactional method.")
        if transaction_is_open:
            tx_holder.close()
            delattr(service, _TX_HOLDER_ATTRIBUTE)
            logger.debug("Closing TX session.")


def transactional(f: Callable) -> Callable:
    """
    Decorator for making a function transactional.

    :param f: Function to decorate.
    :return: Decorated function.

    .. code-block:: python

        from zsl.service import transactional

        class MyService(Service):
            @transactional
            def my_function(self):
                self._repository.create(self._orm, 2, 3, 4)
    """

    @wraps(f)
    def transactional_f(service, *args, **kwargs):
        with tx_session(service):
            return f(service, *args, **kwargs)

    return transactional_f


def set_current_db_node_context(node_name: str | None) -> None:
    """
    Set the current database node context.

    :param node_name: Name of the node.
    """
    context = DbNodeContext(node_name)

    DbNodeContext.set_current_context(context)


def use_db_master_node(f: Callable) -> Callable:
    """
    Decorator for setting thread context to force use master node for db.
    Needs to be executed before first transactional/tx_session call.

    :param f: Function to decorate.
    :return: Decorated function.

    .. code-block:: python

        from zsl.service import use_db_master_node

        class MyService(Service):
            @transactional
            @use_db_master_node
            def my_function(self):
                self._repository.create(self._orm, 2, 3, 4)
    """

    @wraps(f)
    def use_db_master_node_f(service, *args, **kwargs):
        @inject(config=Config)
        def get_config(config):
            return config

        original_context = DbNodeContext.try_getting_current_context()
        try:
            config = get_config()

            set_current_db_node_context(config["DATABASE_MASTER_NODE_NAME"])

            return f(service, *args, **kwargs)
        finally:
            set_current_db_node_context(original_context.node_name if original_context is not None else None)

    return use_db_master_node_f

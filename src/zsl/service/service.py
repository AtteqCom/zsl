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

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session

from zsl import Injected, Zsl, inject
from zsl.application.modules.alchemy_module import EmptyTransactionalHolder, SessionFactory, TransactionHolderFactory

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

    @inject(app=Zsl, engine=Engine)
    def __init__(self, app=Injected, engine=Injected):
        """Constructor - initializes and injects the needed libraries."""
        super(Service, self).__init__()
        self._app = app
        self._engine = engine


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

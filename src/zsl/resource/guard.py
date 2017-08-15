"""
:mod:`zsl.resource.guard`
-------------------------

Guard module defines tools to inject security checks into a resource. With
help of the ``guard`` class decorator and ``ResourcePolicy`` declarative
policy class a complex security resource behaviour can be achieved.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
from enum import Enum
from functools import wraps
import http.client
from typing import Any, Callable, Dict, List, Optional

from future.utils import raise_from

from zsl.interface.resource import ResourceResult
from zsl.service.service import _TX_HOLDER_ATTRIBUTE, SessionFactory, transactional
from zsl.utils.http import get_http_status_code_value

_HTTP_STATUS_FORBIDDEN = get_http_status_code_value(http.client.FORBIDDEN)


class Access(Enum):
    ALLOW = 1
    DENY = 2
    CONTINUE = 3


class ResourcePolicy(object):
    """Declarative policy class.

    Every CRUD method has is corespondent *can_method__before* and
    *can_method__after* where *method* can be one of (*create*, *read*,
    *update*, *delete*). *__before* method will get the CRUD method
    parameters and *__after* will get the CRUD method result as parameter. On
    returning ``Access.ALLOW`` access is granted. It should return
    ``Access.CONTINUE`` when the policy is not met, but is not broken, i. e. it
    is not its responsibility to decide. On returning ``Access.DENY`` or raising
    a ``PolicyException`` policy is broken  and access is immediately denied.

    The default implementation of these method lookup for corresponding
    attribute *can_method*, so ``can_read = Access.ALLOW`` will allow access
    for reading without the declaration of ``can_read__before`` or
    ``can_read__after``. *default* attribute is used if *can_method*
    attribute is not declared. For more complex logic it can be declared as a
    property, see examples:

    .. code-block:: python


        class SimplePolicy(ResourcePolicy):
            '''Allow read and create'''

            default = Access.ALLOW
            can_delete = Access.CONTINUE
            can_update = Access.CONTINUE


        class AdminPolicy(ResourcePolicy):
            '''Only admin has access'''

            @inject(user_service=UserService)
            def __init__(self, user_service):
                self._user_service = user_service

            @property
            def default(self):
                if self._user_service.current_user.is_admin:
                    return Access.ALLOW
    """
    default = Access.CONTINUE

    # can_create

    # can_read

    # can_update

    # can_delete

    def can_create__before(self, *args, **kwargs):
        """Check create method before executing."""
        return self._check_default('can_create')

    def can_create__after(self, *args, **kwargs):
        """Check create method after executing."""
        return self._check_default('can_create')

    def can_read__before(self, *args, **kwargs):
        """Check read method before executing."""
        return self._check_default('can_read')

    def can_read__after(self, *args, **kwargs):
        """Check read method after executing."""
        return self._check_default('can_read')

    def can_update__before(self, *args, **kwargs):
        """Check update method before executing."""
        return self._check_default('can_update')

    def can_update__after(self, *args, **kwargs):
        """Check update method after executing."""
        return self._check_default('can_update')

    def can_delete__before(self, *args, **kwargs):
        """Check delete method before executing."""
        return self._check_default('can_delete')

    def can_delete__after(self, *args, **kwargs):
        """Check delete method after executing."""
        return self._check_default('can_delete')

    def _check_default(self, prop):
        # type: (str) -> Access
        return getattr(self, prop, self.default)


class PolicyViolationError(Exception):
    """Error raised when policy is violated.

    It can bear a HTTP status code, 403 is by default.
    """

    def __init__(self, message, code=_HTTP_STATUS_FORBIDDEN):
        self.code = code
        super(PolicyViolationError, self).__init__(message)


class GuardedMixin(object):
    """Add guarded CRUD methods to resource.

    The ``guard`` replaces the CRUD guarded methods with a wrapper with
    security checks around these methods. It adds this mixin into the
    resource automatically, but it can be declared on the resource manually
    for IDEs to accept calls to the guarded methods.
    """

    def guarded_create(self, params, args, data):
        # type: (str, Dict[str, str], Dict[str, Any]) -> Dict[str, Any]
        pass

    def guarded_read(self, params, args, data):
        # type: (str, Dict[str, str], Dict[str, Any]) -> Dict[str, Any]
        pass

    def guarded_update(self, params, args, data):
        # type: (str, Dict[str, str], Dict[str, Any]) -> Dict[str, Any]
        pass

    def guarded_delete(self, params, args, data):
        # type: (str, Dict[str, str], Dict[str, Any]) -> Dict[str, Any]
        pass


def default_error_handler(e, *_):
    # type: (PolicyViolationError, Any) -> ResourceResult
    """Default policy violation error handler.

    It will create an empty resource result with an error HTTP code.
    """

    return ResourceResult(
        status=e.code,
        body={}
    )


class guard(object):
    """Guard decorator.

    This decorator wraps the CRUD methods with security checks before and
    after CRUD method execution, so that the response can be stopped or
    manipulated. The original CRUD methods are renamed to *guarded_method*,
    where *method* can be [*create*, *read*, *update*, *delete*], so by using a
    `GuardedResource` as a base, you can still redeclare the *guarded_methods*
    and won't loose the security checks.

    It takes a list of policies, which will be always checked before and
    after executing the CRUD method.

    Policy is met, when it returns ``Access.ALLOW``, on ``Access.CONTINUE`` it
    will continue to check others and on ``Access.DENY`` or raising a
    ``PolicyViolationError`` access will be restricted. If there is no policy
    which grants the access a ``PolicyViolationError`` is raised and access
    will be restricted.

    Guard can have a custom exception handlers or method wrappers to _wrap the
    CRUD method around.

    .. code-block:: python


        class Policy(ResourcePolicy):
            default = Access.DENY
            can_read = Access.ALLOW  # allow only read


        @guard([Policy()])
        class GuardedResource(GuardedMixin):
            def read(self, param, args, data):
                return resources[param]


        class SpecificResource(GuardedResource):
            # override GuardedResource.read, but with its security checks
            def guarded_read(self, param, args, data):
                return specific_resources[param]

    """
    method_wrappers = []
    exception_handlers = [default_error_handler]
    resource_methods = ['create', 'read', 'update', 'delete']

    def __init__(self, policies=None, method_wrappers=None,
                 exception_handlers=None):
        # type: (Optional[List[policies]]) -> None

        self.policies = list(policies) if policies else []

        if method_wrappers:
            self._method_wrappers = self.method_wrappers + method_wrappers
        else:
            self._method_wrappers = list(self.method_wrappers)

        if exception_handlers:
            self._exception_handlers = \
                self.exception_handlers + exception_handlers
        else:
            self._exception_handlers = list(self.exception_handlers)

    @staticmethod
    def _check_before_policies(res, name, *args, **kwargs):
        for policy in res._guard_policies:
            access = _call_before(policy, name)(*args, **kwargs)

            if access == Access.ALLOW:
                return

            elif access == Access.DENY:
                raise PolicyViolationError('Access denied for {} {}'.format(
                    name, 'before'), code=_HTTP_STATUS_FORBIDDEN)

            elif access == Access.CONTINUE:
                continue

            else:
                raise TypeError('Access has no value {}'.format(access))

        raise PolicyViolationError(
            "Access haven't been granted for {} {}".format(
                name, 'before'), code=_HTTP_STATUS_FORBIDDEN)

    @staticmethod
    def _check_after_policies(res, name, result):
        for policy in res._guard_policies:
            access = _call_after(policy, name)(result)

            if access == Access.ALLOW:
                return

            elif access == Access.DENY:
                raise PolicyViolationError('Policy violation for {} {}'.format(
                    name, 'before'), code=_HTTP_STATUS_FORBIDDEN)

            elif access == Access.CONTINUE:
                continue

            else:
                raise TypeError('Access have no value {}'.format(access))

        raise PolicyViolationError(
            "Access haven't been granted for {} {}".format(
                name, 'after'), code=_HTTP_STATUS_FORBIDDEN)

    def _wrap(self, method):
        # type: (Callable) -> Callable

        name = method.__name__

        @wraps(method)
        def wrapped(*args, **kwargs):
            res = args[0]
            args = args[1:]

            try:
                self._check_before_policies(res, name, *args, **kwargs)
                rv = _guarded_method(res, name)(*args, **kwargs)
                self._check_after_policies(res, name, rv)

            except PolicyViolationError as e:
                rv = self._handle_exception(e, res)

            return rv

        for mw in reversed(self._method_wrappers):
            wrapped = mw(wrapped)

        return wrapped

    def _handle_exception(self, error, resource):
        rv = None
        for handler in self._exception_handlers:
            rv = handler(error, rv, resource)

        return rv

    def __call__(self, cls):
        if hasattr(cls, '_guard_policies'):
            self.policies += getattr(cls, '_guard_policies')
            setattr(cls, '_guard_policies', list(self.policies))

            return cls

        setattr(cls, '_guard_policies', list(self.policies))

        for method_name in self.resource_methods:
            guarded_name = _guarded_name(method_name)

            if hasattr(cls, method_name):
                method = getattr(cls, method_name)

                setattr(cls, method_name, self._wrap(method))
                setattr(cls, guarded_name, method)

        if issubclass(cls, GuardedMixin):
            return cls
        else:
            return type(cls.__name__, (cls, GuardedMixin), {})


def transactional_error_handler(e, rv, _):
    # type: (Any, Any, SessionFactory) -> Any
    """Re-raise a violation error to be handled in the
    ``_nested_transactional``.
    """
    raise_from(_TransactionalPolicyViolationError(rv), e)


def _nested_transactional(fn):
    # type: (Callable) -> Callable
    """In a transactional method create a nested transaction."""
    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        # type: (SessionFactory) -> Any

        try:
            rv = fn(self, *args, **kwargs)
        except _TransactionalPolicyViolationError as e:
            getattr(self, _TX_HOLDER_ATTRIBUTE).rollback()
            rv = e.result

        return rv
    return wrapped


class transactional_guard(guard):
    """Security guard for ``ModelResource``.

    This add a transactional method wrapper and error handler which calls the
    rollback on ``PolicyViolationError``.
    """
    method_wrappers = [transactional, _nested_transactional]
    exception_handlers = guard.exception_handlers + [
        transactional_error_handler]


class _TransactionalPolicyViolationError(PolicyViolationError):
    """Exception raised during """
    def __init__(self, result):
        # type: (ResourceResult) -> None
        self.result = result
        super(_TransactionalPolicyViolationError, self).__init__(
            result.body,
            result.status
        )


def _guarded_method(res, method_name):
    # type: (object, str) -> Callable
    """Return the guarded method from CRUD name"""
    return getattr(res, _guarded_name(method_name))


def _guarded_name(method_name):
    # type: (str) -> str
    """Return name for guarded CRUD method.

    >>> _guarded_name('read')
    'guarded_read'
    """
    return 'guarded_' + method_name


def _before_name(method_name):
    # type: (str) -> str
    """Return the name of the before check method.

    >>> _before_name('read')
    'can_read__before'
    """
    return 'can_' + method_name + '__before'


def _after_name(method_name):
    # type: (str) -> str
    """Return the name of after check method.

    >>> _after_name('read')
    'can_read__after'
    """
    return 'can_' + method_name + '__after'


def _call_before(policy, method_name):
    # type: (ResourcePolicy, str) -> Callable
    """Return the before check method.

    >>> p = ResourcePolicy()
    >>> _call_before(p, 'read')
    p.can_read__before
    """
    return getattr(policy, _before_name(method_name))


def _call_after(policy, method_name):
    # type: (ResourcePolicy, str) -> Callable
    """Return the after check method.

    >>> p = ResourcePolicy()
    >>> _call_after(p, 'read')
    p.can_after__before
    """
    return getattr(policy, _after_name(method_name))

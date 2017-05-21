"""
:mod:`zsl.resource.guard`
-------------------------

Guard module defines tools to inject security checks into a resource. With 
help of the ``guard`` class decorator and ``ResourcePolicy`` declarative 
policy class a complex security resource behaviour can be achieved. 
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from typing import List, Optional, Dict, Any, Callable
from functools import wraps

from zsl.interface.resource import ResourceResult
from zsl.service.service import TransactionalSupport, transactional


class ResourcePolicy(object):
    """Declarative policy class.

    Every CRUD method has is corespondent *can_method__before* and 
    *can_method__after* where *method* can be one of (*create*, *read*, 
    *update*, *delete*). *__before* method will get the CRUD method 
    parameters and *__after* will get the CRUD method result as parameter. On 
    returning ``True`` access is granted. It should return ``False`` when 
    the policy is not met, but is not broken, i. e. it is not its 
    responsibility to decide. On raising  `PolicyException`` policy is broken 
    and access is immediately restricted.
      
    The default implementation of these method lookup for corresponding 
    attribute *can_method*, so ``can_read = True`` will allow access for 
    reading without the declaration of ``can_read__before`` or 
    ``can_read__after``. *default* attribute is used if *can_method* 
    attribute is not declared. For more complex logic it can be declared as a 
    property, see examples:

    .. code-block:: python


        class SimplePolicy(ResourcePolicy):
            '''Allow read and create'''
            
            default = True    
            can_delete = False
            can_update = False 
            
            
        class AdminPolicy(ResourcePolicy):
            '''Only admin has access'''
            
            @inject(user_service=UserService)
            def __init__(self, user_service):
                self._user_service = user_service
    
            @property
            def default(self):
                return self._user_service.current_user.is_admin
    """
    default = False

    # can_create

    # can_read

    # can_update

    # can_delete

    def _check_default(self, prop):
        return getattr(self, prop, self.default)

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


class PolicyViolationError(Exception):
    """Error raised when policy is violated.
    
    It can bear a HTTP status code, 403 is by default.
    """
    def __init__(self, message, code=403):
        self.code = code
        super(PolicyViolationError, self).__init__(message)


class GuardedMixin(object):
    """Add secure CRUD methods to resource.
    
    The ``guard`` replaces the CRUD method with a wrapper with 
    security checks around these methods. It adds this mixin into the 
    resource automatically, but it can be declared on the resource manually for 
    IDEs.
    """
    def secure_create(self, params, args, data):
        # type: (str, Dict[str, str], Dict[str, Any]) -> Dict[str, Any]
        pass

    def secure_read(self, params, args, data):
        # type: (str, Dict[str, str], Dict[str, Any]) -> Dict[str, Any]
        pass

    def secure_update(self, params, args, data):
        # type: (str, Dict[str, str], Dict[str, Any]) -> Dict[str, Any]
        pass

    def secure_delete(self, params, args, data):
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
    manipulated. The original CRUD methods are renamed to *secure_method*, 
    where *method* can be [*create*, *read*, *update*, *delete*], so by using a 
    guarder resource as a base, you can still redeclare the *secure_methods* 
    and won't loose the security checks.
    
    It takes a list of policies, which will be always checked before and 
    after executing the CRUD method. 
    
    Policy is met, when it returns ``True``, on ``False`` it will continue to 
    check others and on raising a ``PolicyViolationError`` it will be
    restricted. If there is no policy which grants the access a 
    ``PolicyViolationError`` is raised and access is restricted too. 
    
    Guard can have a custom exception handlers or method wrappers to _wrap the 
    CRUD method around. 
    
    .. code-block:: python
    
    
        class Policy(ResourcePolicy):
            default = False
            can_read = True  # allow only read
    
    
        @guard([Policy()])
        class GuardedResource(GuardedMixin):
            def read(self, param, args, data):
                return resources[param]
                
                
        class SpecificResource(GuardedResource):
            # override GuardedResource.read, but with its security checks
            def secure_read(self, param, args, data):
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
            self._exception_handlers = self.exception_handlers + \
                                       exception_handlers
        else:
            self._exception_handlers = list(self.exception_handlers)

    def _check_before_policies(self, name, *args, **kwargs):
        if not any(_before(p, name)(*args, **kwargs) for p in self.policies):
                raise PolicyViolationError('Policy violation for {} {}'.format(
                    name, 'before'), code=403)

    def _check_after_policies(self, name, result):
        if not any(_after(p, name)(result) for p in self.policies):
                raise PolicyViolationError('Policy violation for {} {}'.format(
                    name, 'after'), code=403)

    def _wrap(self, method):
        # type: (Callable) -> Callable

        name = method.__name__

        @wraps(method)
        def wrapped(*args, **kwargs):
            # type: (GuardedMixin) -> Dict

            try:
                self._check_before_policies(name, *args, **kwargs)
                rv = method(*args, **kwargs)
                self._check_after_policies(name, rv)

            except PolicyViolationError as e:
                res = args[0]
                rv = self._handle_exception(e, res)

            return rv

        for mw in self._method_wrappers:
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
            secure_name = _secure_name(method_name)

            if hasattr(cls, method_name):
                method = getattr(cls, method_name)

                setattr(cls, method_name, self._wrap(method))
                setattr(cls, secure_name, method)

        if issubclass(cls, GuardedMixin):
            return cls
        else:
            return type(cls.__name__, (cls, GuardedMixin), {})


def transactional_error_handler(_, rv, res):
    # type: (Any, Any, TransactionalSupport) -> Any
    """Call rollback in ``ModelResource``,"""
    res._orm.rollback()
    return rv


class transactional_guard(guard):
    """Security guard for ``ModelResource``.
    
    This add a transactional method wrapper and error handler which calls the 
    rollback on ``PolicyViolationError``.
    """
    method_wrappers = [transactional]
    exception_handlers = guard.exception_handlers + [
        transactional_error_handler]


def _secure_name(method_name):
    # type: (str) -> str
    """Return name for secure CRUD method.
    
    >>> _secure_name('read')
    'secure_read'
    """
    return 'secure_' + method_name


def _secure_method(res, method_name):
    # type: (object, str) -> Callable
    """Return the secure method from CRUD name"""
    return getattr(res, _secure_name(method_name))


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


def _before(policy, method_name):
    # type: (ResourcePolicy, str) -> Callable
    """Return the before check method.
    
    >>> p = ResourcePolicy()
    >>> _before(p, 'read')
    p.can_read__before
    """
    return getattr(policy, _before_name(method_name))


def _after(policy, method_name):
    # type: (ResourcePolicy, str) -> Callable
    """Return the after check method.

    >>> p = ResourcePolicy()
    >>> _after(p, 'read')
    p.can_after__before
    """
    return getattr(policy, _after_name(method_name))

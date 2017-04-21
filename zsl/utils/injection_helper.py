"""
:mod:`zsl.utils.injection_helper`
---------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals
from future.utils import viewitems
import injector
from injector import BindingKey, reraise, CallError
import inspect
import functools

from zsl._state import get_current_app


def instantiate(cls):
    inj = get_current_app().injector

    if hasattr(cls, "__new__"):
        task = inj.create_object(cls)
    else:
        task = cls()

    return task


def inject(**bindings):
    """
    Decorator for injecting parameters for ASL objects.
    """

    def outer_wrapper(f):
        def function_wrapper(f):
            for key, value in viewitems(bindings):
                bindings[key] = BindingKey(value)

            @functools.wraps(f)
            def _inject(*args, **kwargs):
                inj = get_current_app().injector
                dependencies = inj.args_to_inject(
                    function=f,
                    bindings=bindings,
                    owner_key=f
                )
                dependencies.update(kwargs)
                try:
                    return f(*args, **dependencies)
                except TypeError as e:
                    reraise(e, CallError(f, args, dependencies, e))

            return _inject

        '''
        Just a convenience method - delegates everything to wrapper.
        '''

        def method_or_class_wrapper(*a, **kwargs):
            """
            Properly installs the injector into the object so that the injection can be performed.
            """
            inj = get_current_app().injector
            # Install injector into the self instance if this is a method call.
            inj.install_into(a[0])

            # Use the generic wrapper.
            inject_f = injector.inject(**bindings)
            # Call the method.
            return inject_f(f)(*a, **kwargs)

        if inspect.getargspec(f)[0][0] == 'self':
            return method_or_class_wrapper
        else:
            return function_wrapper(f)

    return outer_wrapper


def bind(interface, to=None, scope=None):
    get_current_app().injector.binder.bind(interface, to, scope)

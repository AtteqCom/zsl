'''
:mod:`asl.utils.injection_helper`

.. moduleauthor:: Martin Babka
'''
from asl.application.service_application import service_application as _app
import injector
from injector import BindingKey, reraise, CallError
import inspect
import functools

def instantiate(cls):
    injector = _app.get_injector()

    if hasattr(cls, "__new__"):
        task = injector.create_object(cls)
    else:
        task = cls()

    return task

def inject(**bindings):
    '''
    Decorator for injecting parameters for ASL objects.
    '''
    def outer_wrapper(f):
        def function_wrapper(f):
            for key, value in bindings.items():
                bindings[key] = BindingKey(value, None)

            @functools.wraps(f)
            def inject(*args, **kwargs):
                injector = _app.get_injector()
                dependencies = injector.args_to_inject(
                    function=f,
                    bindings=bindings,
                    owner_key=f
                    )
                dependencies.update(kwargs)
                try:
                    return f(*args, **dependencies)
                except TypeError as e:
                    reraise(e, CallError(f, args, dependencies, e))
            return inject

        '''
        Just a convenience method - delegates everything to wrapper.
        '''
        def method_or_class_wrapper(*a, **kwargs):
            '''
            Properly installs the injector into the object so that the injection can be performed.
            '''
            inj = _app.get_injector()
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
    _app.get_injector().binder.bind(interface, to, scope)

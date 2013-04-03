'''
Created on 3.4.2013

@author: Martin Babka
'''
from asl.application.service_application import service_application
import injector

_app = service_application

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
        '''
        Just a convenience method - delegates everything to wrapper.
        '''
        def wrapper(*a, **kwargs):
            '''
            Properly installs the injector into the object so that the injection can be performed.
            '''
            inj = _app.get_injector()
            # Install injector.
            inj.install_into(a[0])
            # Use the generic wrapper.
            inject_f = injector.inject(**bindings)
            # Call the method.
            return inject_f(f)(*a, **kwargs)
        return wrapper

    return outer_wrapper

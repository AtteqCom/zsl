'''
Created on 3.4.2013

@author: Martin Babka
'''
from asl.application.service_application import service_application

_app = service_application

def instantiate(cls):
    injector = _app.get_injector()

    if hasattr(cls, "__new__"):
        task = injector.create_object(cls)
    else:
        task = cls()

    return task

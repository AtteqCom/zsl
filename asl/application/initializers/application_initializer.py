'''
Created on 24.1.2013

@author: Martin Babka
'''
import asl.vendor
import logging
from asl.application.service_application import service_application, AtteqServiceFlask
asl.vendor.do_init()
from injector import singleton
from asl.application.initializers import injection_module

class ApplicationInitializer(object):
    '''
    Application initializer - just for the injection capability.
    '''

    def initialize(self, binder):
        '''
        Initialization method.
        '''
        binder.bind(
            AtteqServiceFlask,
            to = service_application,
            scope = singleton
        )
        service_application.set_injector(binder.injector)
        logger = binder.injector.get(logging.Logger)
        logger.debug("Created AtteqServiceFlask binding.")

@injection_module
def application_initializer_module(binder):
    ApplicationInitializer().initialize(binder)

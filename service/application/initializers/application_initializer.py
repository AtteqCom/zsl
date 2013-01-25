'''
Created on 24.1.2013

@author: Martin Babka
'''
import vendor
import logging
from application.service_application import service_application, SportkyFlask
vendor.do_init()
from injector import singleton
from application.initializers import injection_module

class ApplicationInitializer(object):
    '''
    Application initializer - just for the injection capability.
    '''

    def initialize(self, binder):
        '''
        Initialization method.
        '''
        binder.bind(
            SportkyFlask,
            to = service_application,
            scope = singleton
        )
        service_application.set_injector(binder.injector)
        logger = binder.injector.get(logging.Logger)
        logger.debug("Created SportkyFlask binding.")

@injection_module
def application_initializer_module(binder):
    ApplicationInitializer().initialize(binder)

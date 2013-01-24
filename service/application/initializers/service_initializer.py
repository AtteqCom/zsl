'''
Created on 24.1.2013

@author: Martin Babka
'''
import vendor
import logging
from sportky.service.club_service import ClubService
from sportky.service.sport_service import SportService
from sportky.service.state_service import StateService
vendor.do_init()
from injector import singleton
from application.initializers import injection_module

class ServiceInitializer(object):
    '''
    Initializer handling the service injection.
    '''

    def initialize(self, binder):
        '''
        Initialization method.
        '''
        services = [ClubService, SportService, StateService]

        for cls in services:
            binder.bind(
                cls,
                to = binder.injector.create_object(cls),
                scope = singleton
            )
            logger = binder.injector.get(logging.Logger)
            logger.debug("Created {0} binding.".format(cls))


@injection_module
def application_initializer_module(binder):
    ServiceInitializer().initialize(binder)

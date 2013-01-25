'''
Created on 24.1.2013

@author: Martin Babka
'''
import vendor
from injector import singleton
import logging
from application.initializers import injection_module
from utils.string_helper import camelcase_to_underscore
vendor.do_init()

class ServiceInitializer(object):
    '''
    Initializer handling the service injection.
    '''

    def initialize(self, binder):
        '''
        Initialization method.
        '''
        services = ['ClubService', 'SportService', 'StateService']

        for cls_name in services:
            module_name = camelcase_to_underscore(cls_name)
            package_name = "sportky.service.{0}".format(module_name)
            module = getattr(__import__(package_name).service, module_name)
            cls = getattr(module, cls_name)

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

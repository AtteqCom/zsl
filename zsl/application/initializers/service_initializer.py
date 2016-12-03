from injector import singleton
import logging
from zsl.application.initializers import injection_module
from zsl.utils.string_helper import camelcase_to_underscore
from zsl.application import service_application

import importlib


class ServiceInitializer(object):
    '''
    Initializer handling the service injection.
    '''

    @staticmethod
    def _bind_service(package_name, cls_name, binder):
        module = importlib.import_module(package_name)
        cls = getattr(module, cls_name)

        binder.bind(
            cls,
            to=binder.injector.create_object(cls),
            scope=singleton
        )
        logger = binder.injector.get(logging.Logger)
        logger.debug("Created {0} binding.".format(cls))

    def initialize(self, binder):
        '''
        Initialization method.
        '''
        service_injection_config = service_application.config['SERVICE_INJECTION']

        if not isinstance(service_injection_config, (tuple, list)):
            service_injection_config = (service_injection_config,)

        for si_conf in service_injection_config:
            if isinstance(si_conf, str):
                package_name, cls_name = si_conf.rsplit('.', 1)
                ServiceInitializer._bind_service(package_name, cls_name, binder)
            elif isinstance(si_conf, dict):
                services = si_conf['list']
                service_package = si_conf['package']

                for cls_name in services:
                    module_name = camelcase_to_underscore(cls_name)
                    package_name = "{0}.{1}".format(service_package, module_name)
                    ServiceInitializer._bind_service(package_name, cls_name, binder)


@injection_module
def application_initializer_module(binder):
    ServiceInitializer().initialize(binder)

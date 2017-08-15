"""
:mod:`zsl.application.initializers.service_initializer`
-------------------------------------------------------
"""
from __future__ import unicode_literals

from builtins import object
import importlib
import logging

from injector import Binder, singleton

from zsl import Config, Injected, inject
from zsl.utils.string_helper import camelcase_to_underscore


class ServiceInitializer(object):
    """Add outside services to application injector."""
    @staticmethod
    @inject(binder=Binder)
    def _bind_service(package_name, cls_name, binder=Injected):
        """Bind service to application injector.

        :param package_name: service package
        :type package_name: str
        :param cls_name: service class
        :type cls_name: str
        :param binder: current application binder, injected
        :type binder: Binder
        """
        module = importlib.import_module(package_name)
        cls = getattr(module, cls_name)

        binder.bind(
            cls,
            to=binder.injector.create_object(cls),
            scope=singleton
        )
        logging.debug("Created {0} binding.".format(cls))

    @staticmethod
    @inject(config=Config)
    def initialize(config):
        """Initialize method.

        :param config: current application config, injected
        :type config: Config
        """
        service_injection_config = config.get('SERVICE_INJECTION', ())

        if not isinstance(service_injection_config, (tuple, list)):
            service_injection_config = (service_injection_config,)

        for si_conf in service_injection_config:
            if isinstance(si_conf, str):
                package_name, cls_name = si_conf.rsplit('.', 1)
                ServiceInitializer._bind_service(package_name, cls_name)
            elif isinstance(si_conf, dict):
                services = si_conf['list']
                service_package = si_conf['package']

                for cls_name in services:
                    module_name = camelcase_to_underscore(cls_name)
                    package_name = "{0}.{1}".format(service_package, module_name)
                    ServiceInitializer._bind_service(package_name, cls_name)

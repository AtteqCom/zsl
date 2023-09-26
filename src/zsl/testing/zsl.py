"""
:mod:`zsl.testing.zsl`
----------------------
This module allows for unit testing with a Zsl instance. Use
:class:`.ZslTestCase` as a mixin to create a predefined Zsl instance to be used
while testing. Refer to unit testing section :ref:`unit-testing-zsl-instance`
for an example.
"""
from collections import namedtuple
from functools import partial
import logging

from zsl import Zsl
from zsl._state import set_current_app
from zsl.application.service_application import set_profile
from zsl.configuration import InvalidConfigurationException

ZslTestConfiguration = namedtuple('ZslTestConfiguration',
                                  ['app_name', 'version', 'container',
                                   'profile', 'config_object'])
ZslTestConfiguration.__new__ = partial(ZslTestConfiguration.__new__,
                                       config_object=None,
                                       version=None,
                                       profile=None)


class ZslTestCase:
    ZSL_TEST_CONFIGURATION = None  # type: ZslTestConfiguration

    @classmethod
    def setUpClass(cls):
        if cls.ZSL_TEST_CONFIGURATION is None:
            raise InvalidConfigurationException("Please give a test container "
                                                "specification via 'container' "
                                                "class variable.")

        config = cls.ZSL_TEST_CONFIGURATION  # type: ZslTestConfiguration
        if config.profile:
            set_profile(config.profile)
        app = Zsl(
            config.app_name + "-test",
            version=config.version,
            modules=config.container.modules(),
            config_object=config.config_object
        )
        app.testing = True
        app.debug = True

        logging.getLogger(config.app_name).debug(
            "ZSL test app created {0}.".format(app))

        super(ZslTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        config = cls.ZSL_TEST_CONFIGURATION  # type: ZslTestConfiguration
        logging.getLogger(config.app_name).debug(
            "ZSL test app tear down {0}.".format(config.app_name))
        set_current_app(None)

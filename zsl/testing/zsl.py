"""
:mod:`zsl.testing.zsl`
----------------------
This module allows for unit testing with a Zsl instance. Use 
:class:`.ZslTestCase` as a mixin to create a predefined Zsl instance to be used
while testing. Refer to unit testing section :ref:`unit-testing-zsl-instance`
for an example.
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import *

from collections import namedtuple

import logging
from functools import partial

from zsl import Zsl
from zsl.application.service_application import set_profile
from zsl.configuration import InvalidConfigurationException

ZslTestConfiguration = namedtuple('ZslTestConfiguration',
                                  ['app_name', 'version', 'container',
                                   'profile', 'config_object'])
ZslTestConfiguration.__new__ = partial(ZslTestConfiguration.__new__,
                                       config_object=None,
                                       version=None,
                                       profile=None)


class ZslTestCase(object):
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
        app = Zsl(config.app_name + "-test",
                  version=config.version,
                  modules=config.container.modules(),
                  config_object=config.config_object)
        logging.getLogger(config.app_name).debug(
            "ZSL test app created {0}.".format(app))

        super(ZslTestCase, cls).setUpClass()

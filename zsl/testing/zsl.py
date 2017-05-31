from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import *

from collections import namedtuple

import logging

from zsl import Zsl
from zsl.application.service_application import set_profile
from zsl.configuration import InvalidConfigurationException

ZslTestConfiguration = namedtuple('ZslTestConfiguration',
                                  ['app_name', 'version', 'container',
                                   'profile'])


class ZslTestCase(object):
    ZSL_TEST_CONFIGURATION: ZslTestConfiguration = None

    @classmethod
    def setUpClass(cls):
        super(ZslTestCase, cls).setUpClass()

        if cls.ZSL_TEST_CONFIGURATION is None:
            raise InvalidConfigurationException("Please give a test container "
                                                "specification via 'container' "
                                                "class variable.")

        config: ZslTestConfiguration = cls.ZSL_TEST_CONFIGURATION
        if config.profile:
            set_profile(config.profile)
        app = Zsl(config.app_name + "-test", version=config.version,
                  modules=config.container.modules())
        logging.getLogger(config.app_name).debug(
            "ZSL test app created {0}.".format(app))

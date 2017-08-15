from unittest.case import TestCase

from zsl import Config, inject
from zsl.application.containers.container import IoCContainer
from zsl.testing.db import IN_MEMORY_DB_SETTINGS
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration
from zsl.utils.redis_helper import Keymaker
from zsl.utils.testing import set_test_responder

__author__ = 'peter'

set_test_responder()


class TestKeymaker(ZslTestCase, TestCase):
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        'test_redis_helper',
        container=IoCContainer,
        config_object=IN_MEMORY_DB_SETTINGS
    )

    def test_empty(self):
        keymaker = Keymaker({})

        with self.assertRaises(AttributeError):
            keymaker.a()

        self.assertEqual(len(keymaker.__dict__), 0, "There should be no method in keymaker")

    def test_normal(self):
        keymaker = Keymaker({'a': 'AAA', 'b': 'XX'})

        self.assertEqual(keymaker.a(), 'AAA', "Pure method")
        self.assertEqual(keymaker.b('x', 'y'), 'XX:x:y', "Method with arguments")

        self.assertEqual(keymaker.b('x', None, 'y'), 'XX:x:y', "Method with a None argument")

        self.assertEqual(keymaker.b('x', None, 0, False, 'y'),
                         'XX:x:0:False:y',
                         "Method with a None and falsified arguments")

    def test_with_prefix(self):
        keymaker = Keymaker({'a': 'AAA', 'b': 'XX'}, prefix="testing")

        self.assertEqual(keymaker.a(), 'testing:AAA', "Pure method with prefix")
        self.assertEqual(keymaker.b('x', 'y'), 'testing:XX:x:y', "Method with arguments and prefix")

    @inject(config=Config)
    def test_with_global_prefix(self, config):
        # type: (Config)->None
        config.setdefault('REDIS', {'prefix': 'global_prefix'})

        keymaker = Keymaker({'a': 'AAA', 'b': 'XX'}, prefix="testing")

        self.assertEqual(keymaker.a(), 'global_prefix:testing:AAA', "Pure method with global and local prefix")
        self.assertEqual(keymaker.b('x', 'y'),
                         'global_prefix:testing:XX:x:y',
                         "Method with arguments and global and local prefix")
        config['REDIS']['prefix'] = None

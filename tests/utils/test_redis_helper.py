import unittest
from injector import singleton

from asl.interface.importer import initialize_cli_application
initialize_cli_application()

from asl.interface.run_tests import set_test_responder
from asl.utils.injection_helper import bind
from flask.config import Config
from asl.utils.redis_helper import Keymaker

__author__ = 'peter'

set_test_responder()

def create_config(dictionary):
    config = Config('.')

    o = type('MyO', (object,), {})()
    o.__dict__ = dictionary

    config.from_object(o)

    return config

class TestKeymaker(unittest.TestCase):

    def setUp(self):
        bind(Config, create_config({}))

    def test_empty(self):
        keymaker = Keymaker({})

        with self.assertRaises(AttributeError):
            keymaker.a()

        self.assertEqual(len(keymaker.__dict__), 1, "No method in keymaker")

    def test_normal(self):
        keymaker = Keymaker({'a': 'AAA', 'b': 'XX'})

        self.assertEqual(keymaker.a(), 'AAA', "Pure method")
        self.assertEqual(keymaker.b('x', 'y'), 'XX:x:y', "Method with arguments")

        self.assertEqual(keymaker.b('x', None, 'y'), 'XX:x:y', "Method with a None argument")

        self.assertEqual(keymaker.b('x', None, 0, False, 'y'),
                         'XX:x:0:False:y',
                         "Method with a None and falsy arguments")

    def test_with_prefix(self):
        keymaker = Keymaker({'a': 'AAA', 'b': 'XX'}, prefix="unittest")

        self.assertEqual(keymaker.a(), 'unittest:AAA', "Pure method with prefix")
        self.assertEqual(keymaker.b('x', 'y'), 'unittest:XX:x:y', "Method with arguments and prefix")

    def test_with_global_prefix(self):
        bind(Config, create_config({'REDIS': {'prefix': 'global_prefix'}}))

        keymaker = Keymaker({'a': 'AAA', 'b': 'XX'}, prefix="unittest")

        self.assertEqual(keymaker.a(), 'global_prefix:unittest:AAA', "Pure method with global and local prefix")
        self.assertEqual(keymaker.b('x', 'y'),
                         'global_prefix:unittest:XX:x:y',
                         "Method with arguments and global and local prefix")

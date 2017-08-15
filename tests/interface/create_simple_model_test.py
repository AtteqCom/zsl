from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *  # NOQA
from unittest.case import TestCase

from zsl.interface.task import create_simple_model


class ParentClass(object):
    pass


class CreateSimpleModelTestCase(TestCase):
    def testCreateSimpleModelWithDefaults(self):
        point = create_simple_model('Point', ['x', 'y'], {'x': 0.0, 'y': 1.0})
        p = point()
        self.assertIsInstance(p, object, "Point must be instance of object.")
        self.assertEqual(p.x, 0.0, "Zero is default for x")
        self.assertEqual(p.y, 1.0, "One is default for y")

    def testCreateSimpleModelWithParent(self):
        point = create_simple_model('Point', ['x', 'y'], parent=ParentClass)
        p = point()
        self.assertIsInstance(p, ParentClass,
                              "Point must be instance of ParentClass.")

    def testCreateSimpleModelWithModule(self):
        module_mock = 0
        point = create_simple_model('Point', ['x', 'y'], parent=ParentClass,
                                    model_module=module_mock)
        p = point()
        self.assertEqual(module_mock, p.__module__)
        self.assertIsInstance(p, ParentClass,
                              "Point must be instance of ParentClass.")

    def testCreateSimpleModelWithoutDefaults(self):
        point = create_simple_model('Point', ['x', 'y'])
        p = point()
        self.assertIsNone(p.x, "None is default")
        self.assertIsNone(p.y, "None is default")

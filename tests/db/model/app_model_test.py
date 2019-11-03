from __future__ import absolute_import, division, print_function, unicode_literals

from unittest import TestCase

from zsl.db.model import AppModel
from zsl.db.model.app_model import RELATED_FIELDS, RELATED_FIELDS_CLASS


class TreeNodeAppModel(AppModel):
    pass


class CreateSimpleModelTestCase(TestCase):

    def testAppModelHints(self):
        model = TreeNodeAppModel(
            {
                'left': {'left': 0, 'op': '+', 'right': 1},
                'op': '*',
                'right': {'left': 3, 'op': '-', 'right': 2}
            },
            hints={
                RELATED_FIELDS: {
                    'left': {
                        RELATED_FIELDS_CLASS: TreeNodeAppModel
                    },
                    'right': {
                        RELATED_FIELDS_CLASS: TreeNodeAppModel
                    }
                }
            }
        )

        self.assertEqual('*', model.op)
        self.assertIsNotNone(model.left)
        self.assertIsNotNone(model.right)

        self.assertEqual('+', model.left.op)
        self.assertEqual('-', model.right.op)

        self.assertEqual(0, model.left.left)
        self.assertEqual(1, model.left.right)

        self.assertEqual(3, model.right.left)
        self.assertEqual(2, model.right.right)

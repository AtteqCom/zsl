from unittest.case import TestCase

from zsl.router.task import TaskConfiguration


def task_factory():
    pass


class TaskConfigurationTestCase(TestCase):
    def testNamespaces(self):
        c = TaskConfiguration().create_namespace('n1').add_packages(['p1']).add_routes(
            {'r1': task_factory}).get_configuration()
        self.assertEqual(1, len(c.namespaces))
        self.assertEqual('n1', c.namespaces[0].namespace)
        self.assertEqual(['p1'], c.namespaces[0].get_packages())
        self.assertEqual({'r1': task_factory}, c.namespaces[0].get_routes())

        c = c.create_namespace('aa').get_configuration()
        self.assertEqual(2, len(c.namespaces))

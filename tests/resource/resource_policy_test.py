"""
Test resource policies.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
import sys
from typing import AnyStr
from unittest import TestCase

from zsl.resource.guard import Access, ResourcePolicy


def class_name(str_):
    # type: (str) -> AnyStr
    """Get name for `type` constructor with correct str type."""
    if sys.version_info.major == 2:
        return bytes(str_, 'utf-8')

    return str_


class TestResourcePolicy(TestCase):
    methods = ['create', 'read', 'update', 'delete']

    def testDefault(self):
        class TestPolicy(ResourcePolicy):
            pass

        policy = TestPolicy()

        self.assertEqual(Access.CONTINUE, policy.can_create__before(),
                         "should always return Access.CONTINUE")
        self.assertEqual(Access.CONTINUE, policy.can_create__after(),
                         "should always return Access.CONTINUE")
        self.assertEqual(Access.CONTINUE, policy.can_read__before(),
                         "should always return Access.CONTINUE")
        self.assertEqual(Access.CONTINUE, policy.can_read__after(),
                         "should always return Access.CONTINUE")
        self.assertEqual(Access.CONTINUE, policy.can_update__before(),
                         "should always return Access.CONTINUE")
        self.assertEqual(Access.CONTINUE, policy.can_update__after(),
                         "should always return Access.CONTINUE")
        self.assertEqual(Access.CONTINUE, policy.can_delete__before(),
                         "should always return Access.CONTINUE")
        self.assertEqual(Access.CONTINUE, policy.can_delete__after(),
                         "should always return Access.CONTINUE")

    def testDefaultSetter(self):
        class TestPolicy(ResourcePolicy):
            default = Access.ALLOW

        policy = TestPolicy()

        self.assertEqual(Access.ALLOW, policy.can_create__before(),
                         "should always return Access.CONTINUE")
        self.assertEqual(Access.ALLOW, policy.can_create__after(),
                         "should always return Access.CONTINUE")
        self.assertEqual(Access.ALLOW, policy.can_read__before(),
                         "should always return Access.CONTINUE")
        self.assertEqual(Access.ALLOW, policy.can_read__after(),
                         "should always return Access.CONTINUE")
        self.assertEqual(Access.ALLOW, policy.can_update__before(),
                         "should always return Access.CONTINUE")
        self.assertEqual(Access.ALLOW, policy.can_update__after(),
                         "should always return Access.CONTINUE")
        self.assertEqual(Access.ALLOW, policy.can_delete__before(),
                         "should always return Access.CONTINUE")
        self.assertEqual(Access.ALLOW, policy.can_delete__after(),
                         "should always return Access.CONTINUE")

    def testCanProperty(self):
        for method in self.methods:
            # dynamically creates
            #
            # class TestPolicy(ResourcePolicy):
            #   can_'method' = Access.ALLOW
            #
            TestPolicy = type(class_name('TestPolicy'), (ResourcePolicy,),
                              {'can_' + method: Access.ALLOW})

            policy = TestPolicy()

            self.assertEqual(
                Access.ALLOW,
                getattr(policy, 'can_{}__before'.format(method))(),
                "should return Access.ALLOW for before {}".format(method)
            )
            self.assertEqual(
                Access.ALLOW,
                getattr(policy, 'can_{}__after'.format(method))(),
                "should return Access.ALLOW for after {}".format(method)
            )

            for m in filter(lambda x: x != method, self.methods):
                self.assertEqual(
                    Access.CONTINUE,
                    getattr(policy, 'can_{}__before'.format(m))(),
                    "should return Access.CONTINUE for before {}".format(method)
                )
                self.assertEqual(
                    Access.CONTINUE,
                    getattr(policy, 'can_{}__after'.format(m))(),
                    "should return Access.CONTINUE for after {}".format(method)
                )

    def testBeforeAndAfterMethods(self):
        for method in self.methods:
            for suffix in ['before', 'after']:
                # dynamically creates
                #
                # class TestPolicy(ResourcePolicy):
                #   def can_'method'__'suffix'(self, *args, **kwargs):
                #       return Access.ALLOW
                #
                TestPolicy = type(
                    class_name('TestPolicy'),
                    (ResourcePolicy,),
                    {
                        'can_{}__{}'.format(method, suffix):
                            lambda _: Access.ALLOW
                    }
                )

                policy = TestPolicy()

                self.assertEqual(
                    Access.ALLOW,
                    getattr(policy, 'can_{}__{}'.format(method, suffix))(),
                    "should return true for {} {}".format(method, suffix)
                )

                for m in self.methods:
                    for s in ['before', 'after']:
                        if m == method and s == suffix:
                            continue

                        self.assertEqual(
                            Access.CONTINUE,
                            getattr(policy, 'can_{}__{}'.format(m, s))(),
                            "should return Access.CONTINUE for {} and {}"
                            .format(m, s)
                        )

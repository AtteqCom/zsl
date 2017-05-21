"""
Test resource policies.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from unittest import TestCase

from zsl.resource.guard import ResourcePolicy


class TestResourcePolicy(TestCase):
    methods = ['create', 'read', 'update', 'delete']

    def testDefault(self):
        class TestPolicy(ResourcePolicy):
            pass

        policy = TestPolicy()

        self.assertFalse(
            policy.can_create__before() and
            policy.can_create__after() and
            policy.can_read__before() and
            policy.can_read__after() and
            policy.can_update__before() and
            policy.can_update__after() and
            policy.can_delete__before() and
            policy.can_delete__after(),
            "should always return false"
        )

    def testDefaultSetter(self):
        class TestPolicy(ResourcePolicy):
            default = True

        policy = TestPolicy()

        self.assertTrue(
            policy.can_create__before() and
            policy.can_create__after() and
            policy.can_read__before() and
            policy.can_read__after() and
            policy.can_update__before() and
            policy.can_update__after() and
            policy.can_delete__before() and
            policy.can_delete__after(),
            "should always return true"
        )

    def testCanProperty(self):
        for method in self.methods:
            # dynamically creates
            #
            # class TestPolicy(ResourcePolicy):
            #   can_'method' = True
            #
            TestPolicy = type('TestPolicy', (ResourcePolicy,),
                              {'can_' + method: True})

            policy = TestPolicy()

            self.assertTrue(
                getattr(policy, 'can_%s__before' % method)() and
                getattr(policy, 'can_%s__after' % method)(),
                "should return true for %s" % method
            )

            for m in filter(lambda x: x != method, self.methods):
                self.assertFalse(
                    getattr(policy, 'can_%s__before' % m)() and
                    getattr(policy, 'can_%s__after' % m)(),
                    "should return false for %s" % m
                )

    def testBeforeAndAfterMethods(self):
        for method in self.methods:
            for suffix in ['before', 'after']:
                # dynamically creates
                #
                # class TestPolicy(ResourcePolicy):
                #   def can_'method'__'suffix'(self, *args, **kwargs):
                #       return True
                #
                TestPolicy = type(
                    'TestPolicy',
                    (ResourcePolicy,),
                    {'can_%s__%s' % (method, suffix): lambda _: True}
                )

                policy = TestPolicy()

                self.assertTrue(
                    getattr(policy, 'can_%s__%s' % (method, suffix))(),
                    "should return true for %s %s" % (method, suffix)
                )

                for m in self.methods:
                    for s in ['before', 'after']:
                        if m == method and s == suffix:
                            continue

                        self.assertFalse(
                            getattr(policy, 'can_%s__%s' % (m, s))() and
                            "should return false for %s and %s" % (m, s)
                        )

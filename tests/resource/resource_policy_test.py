"""
Test resource policies.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from unittest import TestCase
from typing import AnyStr
import sys

from zsl.resource.guard import ResourcePolicy


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
            TestPolicy = type(class_name('TestPolicy'), (ResourcePolicy,),
                              {'can_' + method: True})

            policy = TestPolicy()

            self.assertTrue(
                getattr(policy, 'can_{}__before'.format(method))() and
                getattr(policy, 'can_{}__after'.format(method))(),
                "should return true for {}".format(method)
            )

            for m in filter(lambda x: x != method, self.methods):
                self.assertFalse(
                    getattr(policy, 'can_{}__before'.format(m))() and
                    getattr(policy, 'can_{}__after'.format(m))(),
                    "should return false for {}".format(m)
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
                    class_name('TestPolicy'),
                    (ResourcePolicy,),
                    {'can_{}__{}'.format(method, suffix): lambda _: True}
                )

                policy = TestPolicy()

                self.assertTrue(
                    getattr(policy, 'can_{}__{}'.format(method, suffix))(),
                    "should return true for {} {}".format(method, suffix)
                )

                for m in self.methods:
                    for s in ['before', 'after']:
                        if m == method and s == suffix:
                            continue

                        self.assertFalse(
                            getattr(policy, 'can_{}__{}'.format(m, s))() and
                            "should return false for {} and {}".format(m, s)
                        )

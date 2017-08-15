"""
Test resource guard.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
import inspect
from unittest import TestCase

from zsl.resource.guard import Access, GuardedMixin, ResourcePolicy, guard

try:
    import unittest.mock as mock
except ImportError:
    import mock


_methods = ['create', 'read', 'update', 'delete']

TEST_VALUE_CREATED = 'created'
TEST_VALUE_READ = 'read'
TEST_VALUE_UPDATED = 'updated'
TEST_VALUE_DELETED = 'deleted'


class AccessError(Exception):
    """Because this is not a subtype of PolicyViolationError it should be not
    caught by the default exception handler, so we can test it with an assert.
    """
    pass


class TestResourceGuard(TestCase):
    def setUp(self):
        class PlainResource(object):
            def create(self):
                return TEST_VALUE_CREATED

            def read(self):
                return TEST_VALUE_READ

            def update(self):
                return TEST_VALUE_UPDATED

            def delete(self):
                return TEST_VALUE_DELETED

        class ToBeSecuredResource(PlainResource, GuardedMixin):
            pass

        self.PlainResource = PlainResource
        self.ToBeSecuredResource = ToBeSecuredResource

    @staticmethod
    def _createMockPolicy(before_side_effect=None, after_side_effect=None):
        policy = ResourcePolicy()

        for m in _methods:
            before = 'can_%s__before' % m
            after = 'can_%s__after' % m
            setattr(policy, before, mock.Mock(
                return_value=Access.ALLOW,
                side_effect=before_side_effect,
                name=before
            ))
            setattr(policy, after, mock.Mock(
                return_value=Access.ALLOW,
                side_effect=after_side_effect,
                name=after
            ))

        return policy

    def testAddGuardedMixin(self):
        test_resource_cls = guard([])(self.PlainResource)

        self.assertTrue(
            issubclass(test_resource_cls, GuardedMixin),
            'should create a new class with GuardedMixin in its base'
        )

        self.assertNotEqual(self.PlainResource, test_resource_cls,
                            'should create a new class')

    def testForGuardedMethods(self):
        test_resource_cls = guard([])(self.PlainResource)
        test_resource = test_resource_cls()

        for method in ['create', 'read', 'update', 'delete']:
            m_name = 'guarded_%s' % method
            self.assertTrue(hasattr(test_resource, m_name) and
                            inspect.ismethod(getattr(test_resource, m_name)),
                            'should have %s method' % m_name)

    def testDontModifyTheClassWhenTheMixinIsPresent(self):
        test_resource_cls = guard([])(self.ToBeSecuredResource)

        self.assertEqual(self.ToBeSecuredResource, test_resource_cls,
                         'should not create a new class when GuardedMixin is in'
                         ' the bases')

    def testShouldAllowAccess(self):
        class PermissivePolicy(ResourcePolicy):
            default = Access.ALLOW

        policy = PermissivePolicy()
        test_resource_cls = guard([policy])(self.ToBeSecuredResource)
        resource = test_resource_cls()

        self.assertEqual(TEST_VALUE_CREATED, resource.create(),
                         'should execute create and return value')
        self.assertEqual(TEST_VALUE_READ, resource.read(),
                         'should execute read and return value')
        self.assertEqual(TEST_VALUE_UPDATED, resource.update(),
                         'should execute update and return value')
        self.assertEqual(TEST_VALUE_DELETED, resource.delete(),
                         'should execute delete and return value')

    def testApplyTwice(self):
        policy_1 = [1, 2, 3]
        policy_2 = [4, 5, 6]
        all_policies = policy_2 + policy_1

        test_resource_cls = guard(policy_2)(
            guard(policy_1)(
                self.ToBeSecuredResource
            )
        )

        self.assertListEqual(all_policies, test_resource_cls._guard_policies,
                             'should join guard policies')

    def testDenyWithException(self):
        class ForbiddenPolicy(ResourcePolicy):
            @property
            def default(self):
                raise AccessError

        policy = ForbiddenPolicy()
        test_resource_cls = guard([policy])(self.ToBeSecuredResource)
        resource = test_resource_cls()

        with self.assertRaises(AccessError):
            resource.create()

        with self.assertRaises(AccessError):
            resource.read()

        with self.assertRaises(AccessError):
            resource.update()

        with self.assertRaises(AccessError):
            resource.delete()

    def testErrorHandler(self):
        class ForbiddenPolicy(ResourcePolicy):
            default = Access.DENY

        error_result = 'handled'

        def exc_handler(*_):
            return error_result

        test_resource_cls = guard(
            policies=[ForbiddenPolicy()],
            exception_handlers=[exc_handler]
        )(self.ToBeSecuredResource)
        resource = test_resource_cls()

        self.assertEqual(error_result, resource.create(),
                         'should execute the handler and return an error value')
        self.assertEqual(error_result, resource.read(),
                         'should execute the handler and return an error value')
        self.assertEqual(error_result, resource.update(),
                         'should execute the handler and return an error value')
        self.assertEqual(error_result, resource.delete(),
                         'should execute the handler and return an error value')

    def testCallAfterAndBeforeCallbacks(self):
        policy = self._createMockPolicy()

        class TestResource(self.ToBeSecuredResource):
            def create(self):
                policy.can_create__before.assert_called()
                policy.can_create__after.assert_not_called()

            def read(self):
                policy.can_read__before.assert_called()
                policy.can_read__after.assert_not_called()

            def update(self):
                policy.can_update__before.assert_called()
                policy.can_update__after.assert_not_called()

            def delete(self):
                policy.can_delete__before.assert_called()
                policy.can_delete__after.assert_not_called()

        test_resource_cls = guard([policy])(TestResource)
        resource = test_resource_cls()

        resource.create()
        policy.can_create__before.assert_called()

        resource.read()
        policy.can_create__before.assert_called()

        resource.update()
        policy.can_create__before.assert_called()

        resource.delete()
        policy.can_delete__before.assert_called()

    def testWrappers(self):
        def transform_value(str_):
            return 'transfered_' + str_

        def wrapper(fn):
            def wrapped(*args, **kwargs):
                rv = fn(*args, **kwargs)

                return transform_value(rv)

            return wrapped

        class PermissivePolicy(ResourcePolicy):
            default = Access.ALLOW

        policy = PermissivePolicy()
        test_resource_cls = guard(
            policies=[policy],
            method_wrappers=[wrapper]
        )(self.ToBeSecuredResource)

        resource = test_resource_cls()

        self.assertEqual(transform_value(TEST_VALUE_CREATED), resource.create(),
                         'should transform the value')
        self.assertEqual(transform_value(TEST_VALUE_READ), resource.read(),
                         'should transform the value')
        self.assertEqual(transform_value(TEST_VALUE_UPDATED), resource.update(),
                         'should transform the value')
        self.assertEqual(transform_value(TEST_VALUE_DELETED), resource.delete(),
                         'should transform the value')

    def testPolicyChaining(self):
        class AllowReadPolicy(ResourcePolicy):
            can_read = Access.ALLOW

        class AllowUpdatePolicy(ResourcePolicy):
            can_update = Access.ALLOW

        class DenyDeletePolicy(ResourcePolicy):
            can_delete = Access.DENY

        error_result = 'handled'

        def exc_handler(*_):
            return error_result

        test_resource_cls = guard(
            policies=[AllowReadPolicy(), AllowUpdatePolicy(),
                      DenyDeletePolicy()],
            exception_handlers=[exc_handler]
        )(self.ToBeSecuredResource)

        resource = test_resource_cls()

        self.assertEqual(TEST_VALUE_READ, resource.read(),
                         "should allow to read, because of AllowReadPolicy")
        self.assertEqual(TEST_VALUE_UPDATED, resource.update(),
                         "should allow to update, because of AllowUpdatePolicy")
        self.assertEqual(error_result, resource.create(),
                         "should deny to create, because there\'s no policy "
                         "to allow it")
        self.assertEqual(error_result, resource.delete(),
                         "should deny to delete, because of DenyDeletePolicy")

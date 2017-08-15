"""
Test http responses of resource guard. It should return a model if policy is
met and an proper http code when policy is broken.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
import http.client
from unittest.case import TestCase

from mocks import mock

from zsl import Zsl
from zsl.application.containers.web_container import WebContainer
from zsl.interface.resource import ResourceResult
from zsl.resource.guard import Access, GuardedMixin, PolicyViolationError, ResourcePolicy, guard
from zsl.testing.db import IN_MEMORY_DB_SETTINGS
from zsl.testing.http import HTTPTestCase, json_loads
from zsl.testing.test_utils import parent_module

TEST_VALUE_CREATED = 'created'
TEST_VALUE_READ = 'read'
TEST_VALUE_UPDATED = 'updated'
TEST_VALUE_DELETED = 'deleted'

SAMPLE_MODEL = {
    'test': 'value',
    'one': 1
}


class GuardedResourceTestResource(object):
    """This will be patched."""
    pass


class GuardedResourceTest(TestCase, HTTPTestCase):
    PATH = '/resource/guarded_resource_test'
    RESOURCE_CLASS = 'resource.guarded_resource_test.GuardedResourceTestResource'

    def setUp(self):
        config_object = IN_MEMORY_DB_SETTINGS.copy()
        # add this package as resource package for zsl to find the
        # `JsonServerModelResourceResource`
        config_object['RESOURCE_PACKAGES'] = ('resource',)
        zsl = Zsl(__name__, config_object=config_object,
                  modules=WebContainer.modules())
        zsl.testing = True

        # mock http requests
        self.app = zsl.test_client()

    def testAllowPolicy(self):
        class AllowPolicy(ResourcePolicy):
            default = Access.ALLOW

        @guard([AllowPolicy()])
        class Resource(GuardedMixin):
            def read(self, *args, **kwargs):
                return SAMPLE_MODEL

        with mock.patch(self.RESOURCE_CLASS, Resource):
            rv = self.app.get(self.PATH + '/1')

            self.assertHTTPStatus(
                http.client.OK,
                rv.status_code,
                "should return 200 status, returned data {0}".format(rv.data)
            )
            data = json_loads(rv.data)
            self.assertDictEqual(SAMPLE_MODEL, data,
                                 "should return sample model")

    def testDefaultDenyPolicy(self):
        class DenyPolicy(ResourcePolicy):
            default = Access.DENY

        @guard([DenyPolicy()])
        class Resource(GuardedMixin):
            def read(self, *args, **kwargs):
                return SAMPLE_MODEL

        with mock.patch(self.RESOURCE_CLASS, Resource):
            rv = self.app.get(self.PATH + '/1')
            data = json_loads(rv.data)

            self.assertDictEqual({}, data, "should return an empty model")
            self.assertHTTPStatus(http.client.FORBIDDEN, rv.status_code,
                                  "should return default 403 status")

    def testCustomDenyException(self):
        class PaymentError(PolicyViolationError):
            def __init__(self):
                super(PaymentError, self).__init__('Payment required', code=402)

        class PaymentPolicy(ResourcePolicy):
            @property
            def default(self):
                raise PaymentError()

        @guard([PaymentPolicy()])
        class Resource(GuardedMixin):
            def read(self, *args, **kwargs):
                return SAMPLE_MODEL

        with mock.patch(self.RESOURCE_CLASS, Resource):
            rv = self.app.get(self.PATH + '/1')
            data = json_loads(rv.data)

            self.assertDictEqual({}, data, "should return an empty model")
            self.assertHTTPStatus(http.client.PAYMENT_REQUIRED, rv.status_code,
                                  "should return custom status 402")

    def testCustomErrorHandling(self):
        def error_handler(*_):
            return ResourceResult(body={}, status=301)

        class DenyPolicy(ResourcePolicy):
            default = Access.DENY

        @guard(
            policies=[DenyPolicy()],
            exception_handlers=[error_handler]
        )
        class Resource(GuardedMixin):
            def read(self, *args, **kwargs):
                return SAMPLE_MODEL

        with mock.patch(self.RESOURCE_CLASS, Resource):
            rv = self.app.get(self.PATH + '/1')
            data = json_loads(rv.data)

            self.assertDictEqual({}, data, "should return an empty model")
            self.assertHTTPStatus(http.client.MOVED_PERMANENTLY, rv.status_code,
                                  "should return custom status 301")

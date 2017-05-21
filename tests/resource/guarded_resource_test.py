"""
Test http responses of resource guard. It should return a model if policy is 
met and an proper http code when policy is broken.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

try:
    import unittest.mock as mock
except ImportError:
    import mock

import http.client

from zsl import Zsl
from zsl.application.containers.web_container import WebContainer
from zsl.interface.resource import ResourceResult
from zsl.resource.guard import (guard, GuardedMixin,
                                PolicyViolationError, ResourcePolicy)

from tests.resource.resource_test_helper import test_settings
from tests.test_utils import parent_module, json_loads, HttpTestCase

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


class GuardedResourceTest(HttpTestCase):
    PATH = '/resource/guarded_resource_test'
    RESOURCE_CLASS = __name__ + '.GuardedResourceTestResource'

    def setUp(self):
        zsl = Zsl(__name__, config_object=test_settings,
                  modules=WebContainer.modules())
        zsl.testing = True

        # add this package as resource package for zsl to find the
        # `JsonServerModelResourceResource`
        zsl.config['RESOURCE_PACKAGES'] = (parent_module(__name__),)

        # mock http requests
        self.app = zsl.test_client()

    def testAllowPolicy(self):
        class AllowPolicy(ResourcePolicy):
            default = True

        @guard([AllowPolicy()])
        class Resource(GuardedMixin):
            def read(self, *args, **kwargs):
                return SAMPLE_MODEL

        with mock.patch(self.RESOURCE_CLASS, Resource):
            rv = self.app.get(self.PATH + '/1')
            data = json_loads(rv.data)

            self.assertDictEqual(SAMPLE_MODEL, data,
                                 "should return sample model")
            self.assertHTTPStatus(http.client.OK, rv.status_code,
                                  "should return 200 status")

    def testDefaultDenyPolicy(self):
        class DenyPolicy(ResourcePolicy):
            default = False

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
            default = False

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


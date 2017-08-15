from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *  # NOQA
import http.client
from unittest.case import TestCase

from zsl import Zsl, inject
from zsl.application.containers.web_container import WebContainer
from zsl.application.modules.web.cors import CORSConfiguration
from zsl.interface.web.performers.task import perform_web_task
from zsl.router.task import TaskConfiguration
from zsl.task.task_decorator import crossdomain
from zsl.testing.db import IN_MEMORY_DB_SETTINGS
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration


class TestTask(object):
    @crossdomain('custom-origin', 'm1', 'allow-h', 'expose-h', 21)
    def perform(self, _data):
        return "ok"


class CorsTestCase(ZslTestCase, TestCase):
    CONFIG = IN_MEMORY_DB_SETTINGS.copy()
    CONFIG.update(
        CORS=CORSConfiguration('default-origin', ['default-allow-headers'], ['default-expose-headers'], 42),
        TASKS=TaskConfiguration()
            .create_namespace('n')
                .add_routes({'r': TestTask})
                .get_configuration().
            create_namespace('z')
                .add_packages(['zsl.tasks.zsl'])
                .get_configuration()
    )
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name='CorsTestCase', container=WebContainer,
        config_object=CONFIG)

    @inject(app=Zsl)
    def testNotFound(self, app):
        with app.test_request_context('/'):
            response = perform_web_task('nn', 'r')

            self.assertEqual(http.client.NOT_FOUND,
                             response.status_code,
                             "Status code must be NOT_FOUND.")

            self.assertEqual('default-allow-headers', response.headers['Access-Control-Allow-Headers'])
            self.assertEqual('default-expose-headers', response.headers['Access-Control-Expose-Headers'])
            self.assertEqual('default-origin', response.headers['Access-Control-Allow-Origin'])
            self.assertEqual('42', response.headers['Access-Control-Max-Age'])


    @inject(app=Zsl)
    def testCustom(self, app):
        with app.test_request_context('/'):
            response = perform_web_task('n', 'r')

            self.assertEqual(http.client.OK,
                             response.status_code,
                             "Status code must be OK.")

            self.assertEqual('allow-h', response.headers['Access-Control-Allow-Headers'])
            self.assertEqual('expose-h', response.headers['Access-Control-Expose-Headers'])
            self.assertEqual('custom-origin', response.headers['Access-Control-Allow-Origin'])
            self.assertEqual('21', response.headers['Access-Control-Max-Age'])

from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
import http.client
from unittest.case import TestCase

from zsl import Zsl, inject
from zsl.application.containers.web_container import WebContainer
from zsl.application.modules.web.cors import CORSConfiguration
from zsl.interface.web.performers.task import perform_web_task
from zsl.router.task import TaskConfiguration
from zsl.testing.db import IN_MEMORY_DB_SETTINGS
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration


class TestTask(object):
    def perform(self, _data):
        return "ok"


class TaskRouterTestCase(ZslTestCase, TestCase):
    CONFIG = IN_MEMORY_DB_SETTINGS.copy()
    CONFIG.update(
        CORS=CORSConfiguration('origin'),
        TASKS=TaskConfiguration().create_namespace('n').add_routes(
            {'r': TestTask}).get_configuration().create_namespace('z').add_packages(
            ['zsl.tasks.zsl']).get_configuration()
    )
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name='ErrorHandlingTestCase', container=WebContainer,
        config_object=CONFIG)

    @inject(app=Zsl)
    def testRoutingRoutes(self, app):
        with app.test_request_context('/'):
            response = perform_web_task('n', 'r')

            self.assertEqual(http.client.OK,
                             response.status_code,
                             "Status code must be ok.")
            self.assertEqual('ok', response.data.decode('utf-8'))

    @inject(app=Zsl)
    def testNotFound(self, app):
        with app.test_request_context('/'):
            response = perform_web_task('nn', 'r')

            self.assertEqual(http.client.NOT_FOUND,
                             response.status_code,
                             "Status code must be NOT_FOUND.")

    @inject(app=Zsl)
    def testRoutingPackages(self, app):
        with app.test_request_context('/'):
            response = perform_web_task('z', 'test_task')
            print(response.status_code)
            self.assertEqual(http.client.OK,
                             response.status_code,
                             "Status code must be ok.")
            self.assertEqual('ok', response.data.decode('utf-8'))

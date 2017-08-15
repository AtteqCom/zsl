from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
import http.client
from unittest.case import TestCase

from flask import json

from zsl import Zsl, inject
from zsl.application.containers.web_container import WebContainer
from zsl.application.error_handler import DefaultErrorHandler, ErrorResponse
from zsl.application.modules.web.cors import CORSConfiguration
from zsl.interface.task import fill_model_with_payload
from zsl.interface.web.performers.task import perform_web_task
from zsl.interface.web.utils.execution import execute_web_task
from zsl.router.task import TaskConfiguration
from zsl.task.job_context import WebJobContext
from zsl.testing.db import IN_MEMORY_DB_SETTINGS
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration


class ErrorTask(object):
    def perform(self, _data):
        raise Exception("Test error")


class ErrorHandlingTestCase(ZslTestCase, TestCase):
    CONFIG = IN_MEMORY_DB_SETTINGS.copy()
    CONFIG.update(
        CORS=CORSConfiguration(origin='origin'),
        TASKS=TaskConfiguration()
            .create_namespace('n')
                .add_routes({'r': ErrorTask})
                .get_configuration()
    )
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name='ErrorHandlingTestCase', container=WebContainer,
        config_object=CONFIG)

    @inject(app=Zsl)
    def testErrorTaskExecution(self, app):
        with app.test_request_context('/'):
            with self.assertRaises(Exception):
                jc = WebJobContext(None, None, None, None, None)
                execute_web_task(jc, self._throwError)

            response = perform_web_task('n', 'r')

            self.assertEqual(http.client.INTERNAL_SERVER_ERROR,
                             response.status_code,
                             "Status code must be error.")
            error_response = ErrorResponse(None, None)
            fill_model_with_payload(json.loads(response.data), error_response)
            self.assertEqual(DefaultErrorHandler.ERROR_CODE, error_response.code)
            self.assertTrue('Access-Control-Allow-Origin' in response.headers,
                            "CORS must be set up")
            self.assertEqual('origin',
                             response.headers['Access-Control-Allow-Origin'],
                             "Default origin must be returned.")

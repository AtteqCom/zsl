import http.client
from unittest.case import TestCase

from zsl.task.job_context import JobContext, WebJobContext

from zsl.application.containers.web_container import WebContainer
from zsl.interface.webservice.utils.execution import execute_web_task
from zsl.testing.db import IN_MEMORY_DB_SETTINGS
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration
from zsl import inject, Zsl


class ErrorHandlingTestCase(ZslTestCase, TestCase):
    CONFIG = IN_MEMORY_DB_SETTINGS.copy()
    CONFIG.update(CORS={'origin': 'origin'})
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name='ErrorHandlingTestCase', container=WebContainer,
        config_object=CONFIG)

    @inject(app=Zsl)
    def testErrorTaskExecution(self, app):
        with app.test_request_context('/'):
            jc = WebJobContext(None, None, None, None, None)
            JobContext.set_current_context(jc)
            response = execute_web_task(jc, self._throwError)
            self.assertEqual(http.client.INTERNAL_SERVER_ERROR,
                             response.status_code,
                             "Status code must be error.")
            self.assertTrue('Access-Control-Allow-Origin' in response.headers,
                            "CORS must be set up")
            self.assertEqual('origin',
                             response.headers['Access-Control-Allow-Origin'],
                             "Default origin must be returned.")

    def _throwError(self):
        raise Exception("aa")

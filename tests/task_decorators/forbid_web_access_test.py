import http.client
from unittest import TestCase

from zsl import Zsl, inject
from zsl.application.containers.web_container import WebContainer
from zsl.application.modules.web.cors import CORSConfiguration
from zsl.interface.web.performers.task import perform_web_task
from zsl.router.task import TaskConfiguration
from zsl.task.task_decorator import forbid_web_access
from zsl.testing.db import IN_MEMORY_DB_SETTINGS
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration


class HttpForbiddenTask(object):

    @forbid_web_access
    def perform(self, data):
        return "ok"


class ForbidWebAccessTestCase(ZslTestCase, TestCase):
    CONFIG = IN_MEMORY_DB_SETTINGS.copy()
    CONFIG.update(
        CORS=CORSConfiguration('origin'),
        TASKS=TaskConfiguration().create_namespace('n')
            .add_routes({'r': HttpForbiddenTask}).get_configuration())
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name='ForbidWebAccessTestCase', container=WebContainer,
        config_object=CONFIG)

    @inject(app=Zsl)
    def testHttpAccessToWebForbiddenTask(self, app):
        """

        :param app: Zsl
        :return:
        """

        with app.test_request_context('/'):
            response = perform_web_task('n', 'r')
            self.assertEqual(http.client.FORBIDDEN,
                             response.status_code,
                             "Status code must be 403 (FORBIDDEN).")

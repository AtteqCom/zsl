from __future__ import absolute_import, division, print_function, unicode_literals

import http.client
from builtins import *
from unittest.case import TestCase

from zsl.application.containers.web_container import WebContainer
from zsl.application.modules.web.cors import CORSConfiguration
from zsl.router.task import TaskConfiguration
from zsl.task.task_decorator import secured_task, json_input
from zsl.testing.db import IN_MEMORY_DB_SETTINGS
from zsl.testing.http import HTTPTestCase
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration
from zsl.utils.security_helper import TOKEN_SERVICE_SECURITY_CONFIG, TOKEN_RANDOM, TOKEN_HASHED, compute_token


class SecuredTask(object):

    @json_input
    @secured_task
    def perform(self, data):
        return "ok"


class SecuredTaskTestCase(ZslTestCase, HTTPTestCase, TestCase):
    CONFIG = IN_MEMORY_DB_SETTINGS.copy()
    CONFIG.update({
        'CORS': CORSConfiguration('origin'),
        'TASKS': TaskConfiguration().create_namespace('test').add_routes(
            {'secured_task': SecuredTask}).get_configuration(),
        TOKEN_SERVICE_SECURITY_CONFIG: 'ahoj'
    })

    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name='SecuredTaskTestCase', container=WebContainer,
        config_object=CONFIG)

    def testSecuredTaskWithCorrectSecurityToken(self):
        client = self.getHTTPClient()
        random_token = '1'

        response = self.requestTask(client, 'test/secured_task', {
            'security': {
                TOKEN_RANDOM: random_token,
                TOKEN_HASHED: compute_token(random_token)
            },
        })

        self.assertHTTPStatus(http.client.OK, response.status_code, 'Http status should be 200')

    def testSecuredTaskWithIncorrectSecurityToken(self):
        client = self.getHTTPClient()
        random_token = '1'

        response = self.requestTask(client, 'test/secured_task', {
            'security': {
                TOKEN_RANDOM: random_token,
                TOKEN_HASHED: 'incorrect hash'
            },
        })

        self.assertHTTPStatus(http.client.INTERNAL_SERVER_ERROR, response.status_code, 'Http status should be 500')

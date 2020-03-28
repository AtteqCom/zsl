from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
import http.client
from typing import NamedTuple
from unittest.case import TestCase

from flask import json

from zsl import Zsl, inject
from zsl.application.containers.web_container import WebContainer
from zsl.application.error_handler import DefaultErrorHandler, ErrorResponse
from zsl.application.modules.web.cors import CORSConfiguration
from zsl.db.helpers.pagination import PaginationRequest
from zsl.interface.task import create_simple_model, fill_model_with_payload, payload_into_model
from zsl.interface.web.performers.task import perform_web_task
from zsl.interface.web.utils.execution import execute_web_task
from zsl.router.task import TaskConfiguration
from zsl.task.job_context import WebJobContext
from zsl.task.task_decorator import json_output
from zsl.testing.db import IN_MEMORY_DB_SETTINGS
from zsl.testing.http import HTTPTestCase
from zsl.testing.zsl import ZslTestCase, ZslTestConfiguration


class PaginationParsingTaskResult(object):

    stuffage: str = ""
    page_no: int = 0
    page_size: int = 0


PaginationParsingRequest = create_simple_model(
    'PaginationParsingRequest',
    ['stuffage', 'pagination'],
    {'pagination': PaginationRequest()}
)

_STUFFAGE = "Hello world!"
_PAGE_NO = 6
_PAGE_SIZE = 65


class PaginationParsingTask(object):

    @json_output
    @payload_into_model(PaginationParsingRequest)
    def perform(self, request: PaginationParsingRequest):
        result = PaginationParsingTaskResult()
        result.stuffage = request.stuffage
        result.page_no = request.pagination.page_no
        result.page_size = request.pagination.page_size
        return result


class PaginationParsingTestCase(ZslTestCase, HTTPTestCase, TestCase):
    ZSL_TEST_CONFIGURATION = ZslTestConfiguration(
        app_name='PaginationParsingTestCase',
        container=WebContainer,
        config_object={
            "CORS": CORSConfiguration(origin='origin'),
            "TASKS": TaskConfiguration()
            .create_namespace('n')
            .add_routes({'p': PaginationParsingTask})
            .get_configuration()
        }
    )

    @inject(app=Zsl)
    def testErrorTaskExecution(self, app):
        with self.getHTTPClient() as client:
            random_token = '1'

            response = self.requestTask(
                client,
                '/n/p',
                {
                    "stuffage": _STUFFAGE,
                    "pagination": {
                        "page_no": _PAGE_NO,
                        "page_size": _PAGE_SIZE
                    }
                }
            )

            parsing_response = PaginationParsingTaskResult()
            fill_model_with_payload(json.loads(response.data), parsing_response)

            self.assertEqual(_STUFFAGE, parsing_response.stuffage)
            self.assertEqual(_PAGE_NO, parsing_response.page_no)
            self.assertEqual(_PAGE_SIZE, parsing_response.page_size)

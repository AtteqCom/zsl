"""
:mod:`zsl.testing.http`
-----------------------
This module allows for querying the API via HTTP.
"""
from __future__ import absolute_import, unicode_literals

from builtins import *
import json
from typing import Any, AnyStr, Dict, Union

from flask.testing import FlaskClient
from flask.wrappers import Response

from zsl import Zsl, inject
from zsl.constants import HttpHeaders, MimeType
from zsl.utils.http import get_http_status_code_value


def json_loads(str_):
    # type: (AnyStr) -> Dict[str, str]
    """Parse JSON from Flask response which could be in bytes in Py3."""
    if isinstance(str_, bytes):
        str_ = str_.decode()

    return json.loads(str_)


class HTTPTestCase(object):
    """Extends TestCase with methods for easier testing of HTTP requests."""

    _DEFAULT_REQUEST_TASK_HEADERS = {
        HttpHeaders.CONTENT_TYPE.value: MimeType.APPLICATION_JSON.value
    }

    def requestTask(self, client, task, data, headers=None):
        # type: (FlaskClient, str, dict, dict)->Response
        """
        Request a task using POST and convert the given data to JSON.

        :param client: The client to ZSL which will be used for the request.
        :param task: Url which will be requested using POST method.
        :param data: Data which will be posted and first converted to JSON.
        :param headers: Dictionary of headers that'll be appended the
                        Content-Type: application/json header.
        :return: Flask response.
        """

        if headers is None:
            headers = {}

        headers.update(HTTPTestCase._DEFAULT_REQUEST_TASK_HEADERS)
        return client.post(task, data=json.dumps(data), headers=headers)

    def assertHTTPStatus(self, status, test_value, msg):
        # type: (Union[int, HTTPStatus], int, AnyStr) -> None
        """Assert HTTP status

        :param status: http status
        :param test_value: flask respond status
        :param msg: test message
        """
        status = get_http_status_code_value(status)
        self.assertEqual(status, test_value, msg)

    def assertJSONData(self, rv, data, msg):
        # type: (Response, Any, AnyStr) -> None
        data1 = self.extractResponseJSON(rv)
        self.assertEqual(data1, data, msg)

    def extractResponseJSON(self, rv):
        # type: (Response) -> Dict
        return json.loads(rv.data.decode())

    @inject(app=Zsl)
    def getHTTPClient(self, app):
        # type: (Zsl) -> FlaskClient
        return app.test_client()

    @inject(app=Zsl)
    def getRequestContext(self, app):
        return app.test_request_context()

from __future__ import absolute_import
from __future__ import unicode_literals

import json
from typing import Any
from typing import Dict
from typing import Union

from flask.testing import FlaskClient
from typing import AnyStr

from flask.wrappers import Response

from zsl import inject, Zsl
from zsl.constants import HttpHeaders, MimeType


def json_loads(str_):
    # type: (AnyStr) -> Dict[str, str]
    """Parse json from flask response which could be in bytes in Py3."""
    if isinstance(str_, bytes):
        str_ = str_.decode()

    return json.loads(str_)


class HTTPTestCase(object):
    """Extends TestCase with methods for easier testing of HTTP requests."""

    def requestTask(self, client, task, data, headers=None):
        if headers is None:
            headers = {}

        headers.update({HttpHeaders.CONTENT_TYPE: MimeType.APPLICATION_JSON})
        return client.post(task, data=json.dumps(data), headers=headers)

    def assertHTTPStatus(self, status, test_value, msg):
        # type: (Union[int, HTTPStatus], int, AnyStr) -> None
        """Assert http status

        :param status: http status  
        :param test_value: flask respond status 
        :param msg: test message
        """
        if hasattr(status, 'value'):  # py2/3
            status = status.value
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

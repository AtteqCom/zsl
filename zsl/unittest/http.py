from __future__ import absolute_import
from __future__ import unicode_literals

import json

from zsl import inject, Zsl


def json_loads(str_):
    # type: (AnyStr) -> Dict[str, str]
    """Parse json from flask response which could be in bytes in Py3."""
    if isinstance(str_, bytes):
        str_ = str_.decode()

    return json.loads(str_)


class HttpTestCase:
    """Extends TestCase with methods for easier testing of HTTP requests."""

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

    @inject(app=Zsl)
    def getHTTPClient(self, app):
        # type: (Zsl) -> FlaskClient
        return app.test_client()

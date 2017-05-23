"""
Test utilities.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import json
from unittest import TestCase

def parent_module(module_name):
    # type: (AnyStr) -> AnyStr
    """Return the parent module name for a module.

    :param module_name: module nam
    :type module_name: str
    :return: module's parent name
    :rtype: str

    >>> parent_module('zsl.application.module')
    'zsl.application'
    """
    return '.'.join(module_name.split('.')[:-1])


def json_loads(str_):
    # type: (AnyStr) -> Dict[str, str]
    """Parse json from flask response which could be in bytes in Py3."""
    if isinstance(str_, bytes):
        str_ = str_.decode()

    return json.loads(str_)


class HttpTestCase(TestCase):
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
        self.assertEquals(status, test_value, msg)

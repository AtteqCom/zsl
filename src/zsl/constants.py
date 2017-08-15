from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
from enum import Enum


class MimeType(Enum):
    APPLICATION_JSON = 'application/json'
    # type: str


class HttpHeaders(Enum):
    CONTENT_TYPE = 'Content-Type'
    # type: str

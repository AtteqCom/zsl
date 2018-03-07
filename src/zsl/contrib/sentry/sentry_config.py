from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
from collections import namedtuple
import logging


class SentryConfiguration(namedtuple('SentryConfiguration', ['dsn', 'environment', 'tags', 'register_logging_handler',
                                                             'sentry_logging_handler_level'])):
    __slots__ = ()

    def __new__(cls, dsn, environment=None, tags=None, register_logging_handler=True,
                sentry_logging_handler_level=logging.ERROR):
        tags = [] if tags is None else tags
        return super(SentryConfiguration, cls).__new__(cls, dsn, environment, tags, register_logging_handler,
                                                       sentry_logging_handler_level)

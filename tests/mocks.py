from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from builtins import *

try:
    import unittest.mock as mock
except ImportError:
    import mock

from zsl.service.service import SessionFactory
from zsl.testing.db import TestSessionFactory as DbTestTestSessionFactory
from zsl.utils.injection_helper import bind


def mock_db_session():
    mock_sess = mock.MagicMock()

    class TestSessionFactory(SessionFactory):
        def create_session(self):
            return mock_sess

    bind(SessionFactory, to=TestSessionFactory)
    bind(DbTestTestSessionFactory, to=TestSessionFactory)
    return mock_sess


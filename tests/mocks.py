from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *

from zsl.service.service import SessionFactory
from zsl.testing.db import TestSessionFactory as DbTestTestSessionFactory
from zsl.utils.injection_helper import bind

try:
    import unittest.mock as mock
except ImportError:
    import mock



def mock_db_session():
    mock_sess = mock.MagicMock()

    def session_holder():
        return mock_sess

    class TestSessionFactory(DbTestTestSessionFactory):
        def __init__(self):
            super(TestSessionFactory, self).__init__()
            self._session_holder = session_holder

    bind(SessionFactory, to=TestSessionFactory)
    bind(DbTestTestSessionFactory, to=TestSessionFactory)
    return mock_sess

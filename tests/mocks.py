import unittest.mock as mock

from zsl.service.service import SessionFactory
from zsl.testing.db import TestSessionFactory as DbTestTestSessionFactory
from zsl.utils.injection_helper import bind


def mock_db_session():
    mock_sess = mock.MagicMock()

    def session_holder():
        return mock_sess

    class TestSessionFactory(DbTestTestSessionFactory):
        def __init__(self):
            super().__init__()
            self._session_holder = session_holder

    bind(SessionFactory, to=TestSessionFactory)
    bind(DbTestTestSessionFactory, to=TestSessionFactory)
    return mock_sess

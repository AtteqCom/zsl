import unittest.mock as mock

from zsl import Zsl
from zsl import inject as zsl_inject
from zsl.service.service import SessionFactory
from zsl.testing.db import TestSessionFactory as DbTestTestSessionFactory


@zsl_inject
def mock_db_session(app: Zsl):
    mock_sess = mock.MagicMock()

    def session_holder():
        return mock_sess

    class TestSessionFactory(DbTestTestSessionFactory):
        def __init__(self):
            app.injector.call_with_injection(super(TestSessionFactory, self).__init__)
            self._session_holder = session_holder

    tsf = app.injector.create_object(TestSessionFactory)
    app.injector.binder.bind(SessionFactory, to=tsf)
    app.injector.binder.bind(DbTestTestSessionFactory, to=tsf)
    return mock_sess

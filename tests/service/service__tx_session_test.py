import unittest
from unittest.mock import MagicMock, Mock, patch

from sqlalchemy.orm.session import Session

from zsl.application.modules.alchemy_module import SessionFactory
from zsl.service.service import Service, transactional, tx_session


class TestTxSession(unittest.TestCase):
    def setUp(self):
        self.service = TestTxSession._create_simple_service()

    @patch("zsl.service.service._get_session_factory")
    def test_tx_session__when_called_as_ctx__then_call_commit_close(self, mock_get_session_factory):
        mock_session_factory = Mock(spec=SessionFactory)
        mock_session = Mock(spec=Session)
        mock_session_factory.create_session.return_value = mock_session

        mock_get_session_factory.return_value = mock_session_factory

        with tx_session(self.service) as session:
            self.assertEqual(session, mock_session)

        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    @patch("zsl.service.service._get_session_factory")
    def test_tx_session__when_called_with_exception__then_rollback(self, mock_get_session_factory):
        mock_session_factory = Mock(spec=SessionFactory)
        mock_session = Mock(spec=Session)
        mock_session_factory.create_session.return_value = mock_session

        mock_get_session_factory.return_value = mock_session_factory

        with self.assertRaises(Exception):
            with tx_session(self.service):
                raise Exception("Simulated error")

        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()

    @patch("zsl.service.service.tx_session")
    def test_transactional_decorator__when_called_with_decorator__then_use_tx_session_context(self, mock_tx_session):
        session = Mock(spec=Session)

        ctx_instance = MagicMock()
        ctx_instance.__enter__.return_value = session
        ctx_instance.__exit__.return_value = False

        mock_tx_session.return_value = ctx_instance

        test = self
        class TestService(Service):
            @transactional
            def test_function(self):
                test.assertIsInstance(self, TestService)

        service = TestService()
        service.test_function()

        ctx_instance.__enter__.assert_called_once()
        ctx_instance.__exit__.assert_called_once()

    @patch("zsl.service.service._get_session_factory")
    def test_transactional_decorator__when_called_with_decorator__then_use_set_service_orm(self, mock_get_session_factory):
        mock_session_factory = Mock(spec=SessionFactory)
        mock_session = Mock(spec=Session)
        mock_session_factory.create_session.return_value = mock_session

        mock_get_session_factory.return_value = mock_session_factory

        test = self
        class TestService(Service):
            @transactional
            def test_function(self):
                test.assertEqual(self._orm, mock_session)

        service = TestService()
        service.test_function()

    @staticmethod
    def _create_simple_service() -> Service:
        class SimpleService(Service):
            pass

        return SimpleService()


if __name__ == "__main__":
    unittest.main()

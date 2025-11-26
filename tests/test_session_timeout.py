"""
Unit tests for session timeout functionality.

Tests session timeout logic, activity tracking, and auto-logout behavior.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class MockSessionState:
    """Mock Streamlit session_state for testing."""

    def __init__(self):
        self._state = {}

    def __setitem__(self, key, value):
        self._state[key] = value

    def __getitem__(self, key):
        return self._state[key]

    def get(self, key, default=None):
        return self._state.get(key, default)

    def __contains__(self, key):
        return key in self._state

    def __delitem__(self, key):
        del self._state[key]

    def keys(self):
        return self._state.keys()


class TestSessionTimeoutLogic:
    """Test session timeout logic functions."""

    def test_init_session_timeout_sets_last_activity(self):
        """Test that init_session_timeout sets last_activity_time."""
        from src.ui.auth import init_session_timeout

        session_state = MockSessionState()
        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            init_session_timeout()

            assert 'last_activity_time' in session_state
            assert isinstance(session_state['last_activity_time'], datetime)

    def test_init_session_timeout_does_not_override_existing(self):
        """Test that init_session_timeout doesn't override existing timestamp."""
        from src.ui.auth import init_session_timeout

        session_state = MockSessionState()
        original_time = datetime.now() - timedelta(minutes=5)
        session_state['last_activity_time'] = original_time

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            init_session_timeout()

            assert session_state['last_activity_time'] == original_time

    def test_update_activity_timestamp_updates_time(self):
        """Test that update_activity_timestamp updates the timestamp."""
        from src.ui.auth import update_activity_timestamp

        session_state = MockSessionState()
        old_time = datetime.now() - timedelta(minutes=10)
        session_state['last_activity_time'] = old_time

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            update_activity_timestamp()

            assert session_state['last_activity_time'] > old_time

    def test_get_idle_minutes_returns_correct_duration(self):
        """Test that get_idle_minutes calculates idle time correctly."""
        from src.ui.auth import get_idle_minutes

        session_state = MockSessionState()
        session_state['last_activity_time'] = datetime.now() - timedelta(minutes=15)

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            idle_minutes = get_idle_minutes()

            # Allow small margin for test execution time
            assert 14.9 <= idle_minutes <= 15.1

    def test_get_idle_minutes_no_activity_returns_zero(self):
        """Test that get_idle_minutes returns 0 when no activity time is set."""
        from src.ui.auth import get_idle_minutes

        session_state = MockSessionState()

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            idle_minutes = get_idle_minutes()

            assert idle_minutes == 0

    def test_is_session_expired_returns_true_when_expired(self):
        """Test that is_session_expired returns True after timeout."""
        from src.ui.auth import is_session_expired

        session_state = MockSessionState()
        # Set activity time to 31 minutes ago (default timeout is 30)
        session_state['last_activity_time'] = datetime.now() - timedelta(minutes=31)

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            assert is_session_expired() is True

    def test_is_session_expired_returns_false_when_active(self):
        """Test that is_session_expired returns False within timeout."""
        from src.ui.auth import is_session_expired

        session_state = MockSessionState()
        # Set activity time to 10 minutes ago
        session_state['last_activity_time'] = datetime.now() - timedelta(minutes=10)

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            assert is_session_expired() is False

    def test_is_session_expired_custom_timeout(self):
        """Test that is_session_expired respects custom timeout value."""
        from src.ui.auth import is_session_expired

        session_state = MockSessionState()
        # Set activity time to 11 minutes ago
        session_state['last_activity_time'] = datetime.now() - timedelta(minutes=11)

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state

            # Should not be expired with 15 minute timeout
            assert is_session_expired(timeout_minutes=15) is False

            # Should be expired with 10 minute timeout
            assert is_session_expired(timeout_minutes=10) is True

    def test_is_session_expired_no_activity_not_expired(self):
        """Test that is_session_expired returns False when no activity is recorded."""
        from src.ui.auth import is_session_expired

        session_state = MockSessionState()

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            # Should not expire if no activity time is set (fresh session)
            assert is_session_expired() is False

    def test_should_show_warning_true_near_expiration(self):
        """Test that should_show_warning returns True near expiration."""
        from src.ui.auth import should_show_warning

        session_state = MockSessionState()
        # Set activity time to 29 minutes ago (1 minute before default timeout)
        session_state['last_activity_time'] = datetime.now() - timedelta(minutes=29)

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            assert should_show_warning() is True

    def test_should_show_warning_false_when_active(self):
        """Test that should_show_warning returns False when session is active."""
        from src.ui.auth import should_show_warning

        session_state = MockSessionState()
        # Set activity time to 10 minutes ago
        session_state['last_activity_time'] = datetime.now() - timedelta(minutes=10)

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            assert should_show_warning() is False

    def test_should_show_warning_custom_thresholds(self):
        """Test that should_show_warning respects custom timeout and warning minutes."""
        from src.ui.auth import should_show_warning

        session_state = MockSessionState()
        # Set activity time to 13 minutes ago
        session_state['last_activity_time'] = datetime.now() - timedelta(minutes=13)

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state

            # With timeout=15, warning=2, should show warning at 13 minutes
            assert should_show_warning(timeout_minutes=15, warning_minutes=2) is True

            # With timeout=20, warning=5, should not show warning at 13 minutes
            assert should_show_warning(timeout_minutes=20, warning_minutes=5) is False


class TestSessionTimeoutActions:
    """Test session timeout actions (logout, warning, etc.)."""

    def test_handle_session_timeout_logs_out_when_expired(self):
        """Test that handle_session_timeout logs out user when session is expired."""
        from src.ui.auth import handle_session_timeout

        session_state = MockSessionState()
        session_state['authenticated'] = True
        session_state['user_id'] = 1
        session_state['last_activity_time'] = datetime.now() - timedelta(minutes=31)

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            mock_st.warning = Mock()
            mock_st.rerun = Mock()

            handle_session_timeout()

            # User should be logged out
            assert session_state.get('authenticated') is False
            assert 'user_id' not in session_state

            # Warning should be shown
            mock_st.warning.assert_called_once()

            # Page should rerun
            mock_st.rerun.assert_called_once()

    def test_handle_session_timeout_shows_warning_near_expiration(self):
        """Test that handle_session_timeout shows warning near expiration."""
        from src.ui.auth import handle_session_timeout

        session_state = MockSessionState()
        session_state['authenticated'] = True
        session_state['last_activity_time'] = datetime.now() - timedelta(minutes=29)

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            mock_st.warning = Mock()
            mock_st.button = Mock(return_value=False)
            mock_st.rerun = Mock()

            handle_session_timeout()

            # User should still be authenticated
            assert session_state.get('authenticated') is True

            # Warning should be shown
            mock_st.warning.assert_called()

    def test_handle_session_timeout_extends_session_when_button_clicked(self):
        """Test that handle_session_timeout extends session when extend button is clicked."""
        from src.ui.auth import handle_session_timeout

        session_state = MockSessionState()
        session_state['authenticated'] = True
        old_time = datetime.now() - timedelta(minutes=29)
        session_state['last_activity_time'] = old_time

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            mock_st.warning = Mock()
            mock_st.button = Mock(return_value=True)  # Button clicked
            mock_st.success = Mock()
            mock_st.rerun = Mock()

            handle_session_timeout()

            # Activity time should be updated
            assert session_state['last_activity_time'] > old_time

            # Success message should be shown
            mock_st.success.assert_called()

            # Page should rerun
            mock_st.rerun.assert_called()

    def test_handle_session_timeout_does_nothing_when_active(self):
        """Test that handle_session_timeout does nothing when session is active."""
        from src.ui.auth import handle_session_timeout

        session_state = MockSessionState()
        session_state['authenticated'] = True
        session_state['last_activity_time'] = datetime.now() - timedelta(minutes=10)

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            mock_st.warning = Mock()
            mock_st.rerun = Mock()

            handle_session_timeout()

            # No warning or rerun
            mock_st.warning.assert_not_called()
            mock_st.rerun.assert_not_called()

    def test_handle_session_timeout_skips_when_not_authenticated(self):
        """Test that handle_session_timeout does nothing when user is not authenticated."""
        from src.ui.auth import handle_session_timeout

        session_state = MockSessionState()
        session_state['authenticated'] = False

        with patch('src.ui.auth.st') as mock_st:
            mock_st.session_state = session_state
            mock_st.warning = Mock()
            mock_st.rerun = Mock()

            handle_session_timeout()

            # No warning or rerun
            mock_st.warning.assert_not_called()
            mock_st.rerun.assert_not_called()


class TestTimeoutConfiguration:
    """Test timeout configuration from environment variables."""

    def test_get_timeout_config_uses_default(self):
        """Test that get_timeout_config returns default values."""
        from src.ui.auth import get_timeout_config

        with patch.dict(os.environ, {}, clear=True):
            config = get_timeout_config()

            assert config['timeout_minutes'] == 30
            assert config['warning_minutes'] == 2

    def test_get_timeout_config_uses_environment_variable(self):
        """Test that get_timeout_config uses environment variable when set."""
        from src.ui.auth import get_timeout_config

        with patch.dict(os.environ, {'SESSION_TIMEOUT_MINUTES': '60'}, clear=True):
            config = get_timeout_config()

            assert config['timeout_minutes'] == 60

    def test_get_timeout_config_handles_invalid_env_var(self):
        """Test that get_timeout_config handles invalid environment variable."""
        from src.ui.auth import get_timeout_config

        with patch.dict(os.environ, {'SESSION_TIMEOUT_MINUTES': 'invalid'}, clear=True):
            config = get_timeout_config()

            # Should fall back to default
            assert config['timeout_minutes'] == 30


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

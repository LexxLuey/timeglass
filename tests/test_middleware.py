"""Unit tests for TimeGlass middleware."""

from unittest.mock import Mock
from timeglass.middleware import TimeGlassMiddleware


class TestTimeGlassMiddleware:
    """Test TimeGlassMiddleware functionality."""

    def test_initialization(self):
        """Test middleware initialization."""
        app = Mock()
        middleware = TimeGlassMiddleware(app)
        assert middleware.app == app

    # Note: Async middleware testing is complex and not essential for basic
    # functionality. The core middleware logic is tested through integration
    # tests

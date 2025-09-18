"""Tests for TimeGlass web dashboard."""

import pytest
from fastapi.testclient import TestClient
from timeglass.web import create_app


class TestTimeGlassWeb:
    """Test TimeGlass web dashboard."""

    @pytest.fixture
    def client(self, tmp_path):
        """Create test client with temporary database."""
        db_path = tmp_path / "test.db"
        app = create_app(str(db_path))
        return TestClient(app)

    def test_dashboard_html(self, client):
        """Test dashboard HTML endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "TimeGlass Dashboard" in response.text
        assert "Profiling data visualization" in response.text

    def test_api_stats_empty(self, client):
        """Test stats API with empty database."""
        response = client.get("/api/stats")
        if response.status_code != 200:
            print(f"Error: {response.text}")
        assert response.status_code == 200
        stats = response.json()
        assert stats["total_requests"] == 0
        assert stats["avg_duration_ms"] == 0

    def test_api_requests_empty(self, client):
        """Test requests API with empty database."""
        response = client.get("/api/requests")
        assert response.status_code == 200
        requests = response.json()
        assert requests == []

    def test_api_system_metrics_empty(self, client):
        """Test system metrics API with empty database."""
        response = client.get("/api/system-metrics")
        assert response.status_code == 200
        metrics = response.json()
        assert metrics == []

    def test_request_detail_html(self, client, tmp_path):
        """Test request detail HTML endpoint."""
        from timeglass.storage import TimeGlassStorage
        from timeglass.models import ProfilingMetrics
        from datetime import datetime

        # Use the same database path as the test client
        db_path = tmp_path / "test.db"

        # Create test data
        storage = TimeGlassStorage(str(db_path))
        test_request = ProfilingMetrics(
            request_id="test-123",
            start_time=datetime.fromisoformat("2025-01-01T10:00:00"),
            end_time=datetime.fromisoformat("2025-01-01T10:00:01"),
            duration_ms=100.5,
            cpu_usage_percent=25.0,
            memory_usage_mb=50.0,
            memory_usage_percent=30.0,
            method="GET",
            path="/api/test",
            status_code=200,
            response_size_bytes=1024,
            user_agent="Test Browser",
            client_ip="127.0.0.1",
        )
        storage.save_profiling_metrics(test_request)

        # Test the endpoint
        response = client.get("/request/test-123")
        assert response.status_code == 200
        assert "Request Details" in response.text
        assert "Request ID:" in response.text
        assert "GET" in response.text
        assert "/api/test" in response.text
        assert "200" in response.text

    def test_api_requests_with_filters(self, client):
        """Test requests API with filters."""
        # Test method filter
        response = client.get("/api/requests?method=GET")
        assert response.status_code == 200

        # Test path filter
        response = client.get("/api/requests?path_contains=api")
        assert response.status_code == 200

        # Test status code filter
        response = client.get("/api/requests?status_code=200")
        assert response.status_code == 200

        # Test limit and offset
        response = client.get("/api/requests?limit=10&offset=0")
        assert response.status_code == 200

    def test_api_system_metrics_with_params(self, client):
        """Test system metrics API with parameters."""
        response = client.get("/api/system-metrics?limit=50")
        assert response.status_code == 200

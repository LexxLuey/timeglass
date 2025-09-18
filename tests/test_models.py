"""Unit tests for TimeGlass data models."""

from datetime import datetime
from timeglass.models import ProfilingMetrics, SystemMetrics, QueryMetrics


class TestProfilingMetrics:
    """Test ProfilingMetrics dataclass."""

    def test_creation(self):
        """Test basic creation of ProfilingMetrics."""
        start_time = datetime.now()
        metrics = ProfilingMetrics(
            request_id="test-123",
            start_time=start_time
        )

        assert metrics.request_id == "test-123"
        assert metrics.start_time == start_time
        assert metrics.duration_ms is None
        assert metrics.cpu_usage_percent is None

    def test_serialization(self):
        """Test JSON serialization and deserialization."""
        start_time = datetime.now()
        original = ProfilingMetrics(
            request_id="test-123",
            start_time=start_time,
            duration_ms=150.5,
            cpu_usage_percent=75.2
        )

        # Serialize to dict
        data = original.to_dict()
        assert data["request_id"] == "test-123"
        assert data["duration_ms"] == 150.5
        assert data["cpu_usage_percent"] == 75.2

        # Deserialize from dict
        restored = ProfilingMetrics.from_dict(data)
        assert restored.request_id == original.request_id
        assert restored.duration_ms == original.duration_ms
        assert restored.cpu_usage_percent == original.cpu_usage_percent

    def test_with_all_fields(self):
        """Test ProfilingMetrics with all optional fields."""
        start_time = datetime.now()
        end_time = datetime.now()

        metrics = ProfilingMetrics(
            request_id="test-123",
            start_time=start_time,
            end_time=end_time,
            duration_ms=100.0,
            cpu_usage_percent=50.0,
            memory_usage_mb=256.0,
            memory_usage_percent=25.0,
            method="GET",
            path="/api/test",
            status_code=200,
            response_size_bytes=1024,
            user_agent="TestAgent/1.0",
            client_ip="127.0.0.1"
        )

        assert metrics.method == "GET"
        assert metrics.status_code == 200
        assert metrics.client_ip == "127.0.0.1"


class TestSystemMetrics:
    """Test SystemMetrics dataclass."""

    def test_creation(self):
        """Test basic creation of SystemMetrics."""
        timestamp = datetime.now()
        metrics = SystemMetrics(
            timestamp=timestamp,
            cpu_usage_percent=45.2,
            memory_usage_mb=1024.5,
            memory_usage_percent=60.3,
            total_memory_mb=2048,
            cpu_count=4
        )

        assert metrics.cpu_usage_percent == 45.2
        assert metrics.memory_usage_mb == 1024.5
        assert metrics.cpu_count == 4

    def test_serialization(self):
        """Test JSON serialization."""
        timestamp = datetime.now()
        metrics = SystemMetrics(
            timestamp=timestamp,
            cpu_usage_percent=45.2,
            memory_usage_mb=1024.5,
            memory_usage_percent=60.3,
            total_memory_mb=2048,
            cpu_count=4
        )

        data = metrics.to_dict()
        assert data["cpu_usage_percent"] == 45.2
        assert data["cpu_count"] == 4
        assert "timestamp" in data


class TestQueryMetrics:
    """Test QueryMetrics dataclass."""

    def test_creation(self):
        """Test basic creation of QueryMetrics."""
        timestamp = datetime.now()
        metrics = QueryMetrics(
            request_id="test-123",
            query="SELECT * FROM users",
            duration_ms=25.5,
            timestamp=timestamp
        )

        assert metrics.request_id == "test-123"
        assert metrics.query == "SELECT * FROM users"
        assert metrics.duration_ms == 25.5

    def test_with_connection_id(self):
        """Test QueryMetrics with connection ID."""
        timestamp = datetime.now()
        metrics = QueryMetrics(
            request_id="test-123",
            query="SELECT * FROM users",
            duration_ms=25.5,
            timestamp=timestamp,
            connection_id="conn-456"
        )

        assert metrics.connection_id == "conn-456"

    def test_serialization(self):
        """Test JSON serialization."""
        timestamp = datetime.now()
        metrics = QueryMetrics(
            request_id="test-123",
            query="SELECT * FROM users",
            duration_ms=25.5,
            timestamp=timestamp
        )

        data = metrics.to_dict()
        assert data["request_id"] == "test-123"
        assert data["query"] == "SELECT * FROM users"
        assert data["duration_ms"] == 25.5

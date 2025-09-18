"""Unit tests for TimeGlass storage layer."""

import pytest
from datetime import datetime
from timeglass.storage import TimeGlassStorage
from timeglass.models import ProfilingMetrics, SystemMetrics, QueryMetrics


@pytest.fixture
def temp_db():
    """Create temporary in-memory database for testing."""
    db = TimeGlassStorage(":memory:")
    yield db


class TestTimeGlassStorage:
    """Test TimeGlassStorage functionality."""

    def test_initialization(self, temp_db):
        """Test database initialization."""
        assert temp_db.db_path == ":memory:"

    def test_save_and_retrieve_profiling_metrics(self, temp_db):
        """Test saving and retrieving profiling metrics."""
        start_time = datetime.now()
        metrics = ProfilingMetrics(
            request_id="test-123",
            start_time=start_time,
            duration_ms=150.5,
            cpu_usage_percent=75.2
        )

        # Save metrics
        temp_db.save_profiling_metrics(metrics)

        # Retrieve metrics
        results = temp_db.get_profiling_metrics(limit=1)
        assert len(results) == 1

        retrieved = results[0]
        assert retrieved.request_id == "test-123"
        assert retrieved.duration_ms == 150.5
        assert retrieved.cpu_usage_percent == 75.2

    def test_save_system_metrics(self, temp_db):
        """Test saving system metrics."""
        timestamp = datetime.now()
        metrics = SystemMetrics(
            timestamp=timestamp,
            cpu_usage_percent=45.2,
            memory_usage_mb=1024.5,
            memory_usage_percent=60.3,
            total_memory_mb=2048,
            cpu_count=4
        )

        # Save metrics
        temp_db.save_system_metrics(metrics)

        # Retrieve metrics
        results = temp_db.get_system_metrics(limit=1)
        assert len(results) == 1

        retrieved = results[0]
        assert retrieved.cpu_usage_percent == 45.2
        assert retrieved.memory_usage_mb == 1024.5
        assert retrieved.cpu_count == 4

    def test_save_query_metrics(self, temp_db):
        """Test saving query metrics."""
        timestamp = datetime.now()
        metrics = QueryMetrics(
            request_id="test-123",
            query="SELECT * FROM users",
            duration_ms=25.5,
            timestamp=timestamp
        )

        # Save metrics
        temp_db.save_query_metrics(metrics)

        # Query metrics don't have direct retrieval method in this simple test
        # but the save operation should not fail
        assert True  # If we get here, save succeeded

    def test_get_profiling_metrics_with_limit(self, temp_db):
        """Test retrieving profiling metrics with limit."""
        # Save multiple metrics
        for i in range(5):
            metrics = ProfilingMetrics(
                request_id=f"test-{i}",
                start_time=datetime.now()
            )
            temp_db.save_profiling_metrics(metrics)

        # Retrieve with limit
        results = temp_db.get_profiling_metrics(limit=3)
        assert len(results) == 3

    def test_get_profiling_metrics_empty(self, temp_db):
        """Test retrieving from empty database."""
        results = temp_db.get_profiling_metrics()
        assert len(results) == 0

    def test_stats_summary_empty_db(self, temp_db):
        """Test statistics summary with empty database."""
        stats = temp_db.get_stats_summary()
        assert stats["total_requests"] == 0
        assert stats["avg_duration_ms"] == 0

    def test_stats_summary_with_data(self, temp_db):
        """Test statistics summary with data."""
        # Save some test data
        for i in range(3):
            metrics = ProfilingMetrics(
                request_id=f"test-{i}",
                start_time=datetime.now(),
                duration_ms=100.0 + i * 50,
                cpu_usage_percent=50.0 + i * 10
            )
            temp_db.save_profiling_metrics(metrics)

        stats = temp_db.get_stats_summary()
        assert stats["total_requests"] == 3
        assert stats["avg_duration_ms"] > 0
        assert stats["avg_cpu_percent"] > 0

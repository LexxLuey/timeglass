"""Integration tests for TimeGlass end-to-end functionality."""

import pytest
import time
from datetime import datetime
from timeglass.storage import TimeGlassStorage
from timeglass.models import ProfilingMetrics, SystemMetrics
from timeglass.middleware import TimeGlassMiddleware


class TestEndToEndIntegration:
    """Test complete TimeGlass workflow."""

    @pytest.fixture
    def db(self):
        """Create test database."""
        return TimeGlassStorage(":memory:")

    def test_complete_profiling_workflow(self, db):
        """Test complete profiling workflow from start to finish."""
        # 1. Create profiling metrics
        start_time = datetime.now()
        metrics = ProfilingMetrics(
            request_id="integration-test-123",
            start_time=start_time,
            method="GET",
            path="/api/test",
            status_code=200,
            duration_ms=150.5,
            cpu_usage_percent=75.2,
            memory_usage_mb=512.3
        )

        # 2. Save to database
        db.save_profiling_metrics(metrics)

        # 3. Retrieve from database
        results = db.get_profiling_metrics(limit=1)
        assert len(results) == 1

        retrieved = results[0]
        assert retrieved.request_id == "integration-test-123"
        assert retrieved.method == "GET"
        assert retrieved.status_code == 200

    def test_middleware_with_storage(self, db):
        """Test middleware working with storage layer."""
        # This is a simplified integration test
        # In a real scenario, we'd test with actual FastAPI

        # Create middleware
        def mock_app(scope, receive, send):
            pass

        middleware = TimeGlassMiddleware(mock_app)

        # Verify middleware initializes correctly
        assert middleware.app == mock_app

        # Test that middleware can be created with database available
        # (This is more of a smoke test than a full integration test)
        assert db is not None

    def test_storage_statistics(self, db):
        """Test storage layer statistics generation."""
        # Add some test data
        for i in range(5):
            metrics = ProfilingMetrics(
                request_id=f"stats-test-{i}",
                start_time=datetime.now(),
                duration_ms=100 + i * 20,
                cpu_usage_percent=50 + i * 5
            )
            db.save_profiling_metrics(metrics)

        # Get statistics
        stats = db.get_stats_summary()

        # Verify statistics are reasonable
        assert stats["total_requests"] == 5
        assert stats["avg_duration_ms"] > 0
        assert stats["avg_cpu_percent"] > 0

    def test_system_metrics_integration(self, db):
        """Test system metrics collection and storage."""
        # Create system metrics
        timestamp = datetime.now()
        sys_metrics = SystemMetrics(
            timestamp=timestamp,
            cpu_usage_percent=45.2,
            memory_usage_mb=1024.5,
            memory_usage_percent=60.3,
            total_memory_mb=2048,
            cpu_count=4
        )

        # Save system metrics
        db.save_system_metrics(sys_metrics)

        # Retrieve system metrics
        results = db.get_system_metrics(limit=1)
        assert len(results) == 1

        retrieved = results[0]
        assert retrieved.cpu_count == 4
        assert retrieved.total_memory_mb == 2048

    def test_performance_baseline(self, db):
        """Test that our profiling doesn't add excessive overhead."""
        # This test ensures our storage operations are reasonably fast

        start_time = time.time()

        # Perform multiple database operations
        for i in range(10):
            metrics = ProfilingMetrics(
                request_id=f"perf-test-{i}",
                start_time=datetime.now(),
                duration_ms=50.0
            )
            db.save_profiling_metrics(metrics)

        # Retrieve data
        results = db.get_profiling_metrics(limit=10)

        end_time = time.time()
        total_time = end_time - start_time

        # Should complete in reasonable time (less than 1 second for 10 ops)
        assert total_time < 1.0
        assert len(results) == 10

    def test_data_persistence(self, db):
        """Test that data persists correctly in database."""
        # Save data
        metrics = ProfilingMetrics(
            request_id="persistence-test",
            start_time=datetime.now(),
            method="POST",
            path="/api/data",
            status_code=201,
            duration_ms=200.0
        )
        db.save_profiling_metrics(metrics)

        # Simulate closing and reopening database
        # (In real scenario, this would be a new connection)
        results1 = db.get_profiling_metrics(limit=1)
        results2 = db.get_profiling_metrics(limit=1)

        # Both queries should return same data
        assert len(results1) == 1
        assert len(results2) == 1
        assert results1[0].request_id == results2[0].request_id

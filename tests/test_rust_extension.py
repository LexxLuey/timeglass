"""Unit tests for TimeGlass Rust extension functions."""

import json
import time
from timeglass import start_profiling, stop_profiling, get_system_info


class TestRustExtension:
    """Test Rust extension functions directly."""

    def test_start_profiling_returns_json(self):
        """Test that start_profiling returns valid JSON."""
        result = start_profiling("test-request-123")

        # Should return a JSON string
        assert isinstance(result, str)

        # Should be parseable as JSON
        data = json.loads(result)
        assert isinstance(data, dict)

        # Should contain expected fields
        assert "request_id" in data
        assert "start_time" in data
        assert "cpu_usage_percent" in data
        assert "memory_usage_mb" in data

        # Request ID should match what we passed
        assert data["request_id"] == "test-request-123"

    def test_stop_profiling_calculates_duration(self):
        """Test that stop_profiling calculates request duration."""
        # Start profiling
        start_data_str = start_profiling("duration-test-123")

        # Small delay to ensure measurable duration
        time.sleep(0.01)

        # Stop profiling
        end_data_str = stop_profiling("duration-test-123", start_data_str)
        end_data = json.loads(end_data_str)

        # Should contain duration_ms field
        assert "duration_ms" in end_data
        assert end_data["duration_ms"] > 0

        # Duration should be reasonable (between 1ms and 1000ms for our test)
        assert 1 <= end_data["duration_ms"] <= 1000

    def test_stop_profiling_preserves_request_id(self):
        """Test that stop_profiling preserves the request ID."""
        request_id = "preserve-test-456"
        start_data_str = start_profiling(request_id)

        end_data_str = stop_profiling(request_id, start_data_str)
        end_data = json.loads(end_data_str)

        assert end_data["request_id"] == request_id

    def test_get_system_info_returns_valid_data(self):
        """Test that get_system_info returns system information."""
        result = get_system_info()

        # Should return a JSON string
        assert isinstance(result, str)

        # Should be parseable as JSON
        data = json.loads(result)
        assert isinstance(data, dict)

        # Should contain expected system fields
        assert "total_memory_mb" in data
        assert "cpu_count" in data

        # Values should be reasonable
        assert data["total_memory_mb"] > 0  # Should have some memory
        assert data["cpu_count"] > 0       # Should have at least 1 CPU

    def test_multiple_profiling_calls(self):
        """Test that multiple profiling calls work independently."""
        # First request
        start1 = start_profiling("multi-test-1")
        time.sleep(0.005)
        end1 = stop_profiling("multi-test-1", start1)

        # Second request
        start2 = start_profiling("multi-test-2")
        time.sleep(0.005)
        end2 = stop_profiling("multi-test-2", start2)

        # Parse results
        data1 = json.loads(end1)
        data2 = json.loads(end2)

        # Should have different request IDs
        assert data1["request_id"] != data2["request_id"]

        # Both should have valid durations
        assert data1["duration_ms"] > 0
        assert data2["duration_ms"] > 0

        # Should have CPU and memory data
        assert "cpu_usage_percent" in data1
        assert "memory_usage_mb" in data1
        assert "cpu_usage_percent" in data2
        assert "memory_usage_mb" in data2

    def test_profiling_data_structure(self):
        """Test that profiling data has expected structure."""
        start_data_str = start_profiling("structure-test-789")
        start_data = json.loads(start_data_str)

        time.sleep(0.01)

        end_data_str = stop_profiling("structure-test-789", start_data_str)
        end_data = json.loads(end_data_str)

        # Required fields in start data
        required_start_fields = [
            "request_id", "start_time", "cpu_usage_percent",
            "memory_usage_mb", "memory_usage_percent"
        ]

        for field in required_start_fields:
            assert field in start_data, f"Missing field: {field}"

        # Required fields in end data
        required_end_fields = [
            "request_id", "start_time", "end_time", "duration_ms",
            "cpu_usage_percent", "memory_usage_mb", "memory_usage_percent"
        ]

        for field in required_end_fields:
            assert field in end_data, f"Missing field: {field}"

        # End time should be after start time
        assert end_data["end_time"] > start_data["start_time"]

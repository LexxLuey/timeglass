"""Data models for TimeGlass profiling data."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ProfilingMetrics:
    """Profiling metrics data model."""

    request_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    cpu_usage_percent: Optional[float] = None
    memory_usage_mb: Optional[float] = None
    memory_usage_percent: Optional[float] = None
    method: Optional[str] = None
    path: Optional[str] = None
    status_code: Optional[int] = None
    response_size_bytes: Optional[int] = None
    user_agent: Optional[str] = None
    client_ip: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "request_id": self.request_id,
            "start_time": self.start_time.isoformat() if self.start_time
            else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": self.duration_ms,
            "cpu_usage_percent": self.cpu_usage_percent,
            "memory_usage_mb": self.memory_usage_mb,
            "memory_usage_percent": self.memory_usage_percent,
            "method": self.method,
            "path": self.path,
            "status_code": self.status_code,
            "response_size_bytes": self.response_size_bytes,
            "user_agent": self.user_agent,
            "client_ip": self.client_ip,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProfilingMetrics":
        """Create from dictionary."""
        return cls(
            request_id=data["request_id"],
            start_time=(
                datetime.fromisoformat(data["start_time"])
                if data.get("start_time")
                else None
            ),
            end_time=(
                datetime.fromisoformat(data["end_time"])
                if data.get("end_time")
                else None
            ),
            duration_ms=data.get("duration_ms"),
            cpu_usage_percent=data.get("cpu_usage_percent"),
            memory_usage_mb=data.get("memory_usage_mb"),
            memory_usage_percent=data.get("memory_usage_percent"),
            method=data.get("method"),
            path=data.get("path"),
            status_code=data.get("status_code"),
            response_size_bytes=data.get("response_size_bytes"),
            user_agent=data.get("user_agent"),
            client_ip=data.get("client_ip"),
        )


@dataclass
class SystemMetrics:
    """System-level metrics."""

    timestamp: datetime
    cpu_usage_percent: float
    memory_usage_mb: float
    memory_usage_percent: float
    total_memory_mb: int
    cpu_count: int

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "cpu_usage_percent": self.cpu_usage_percent,
            "memory_usage_mb": self.memory_usage_mb,
            "memory_usage_percent": self.memory_usage_percent,
            "total_memory_mb": self.total_memory_mb,
            "cpu_count": self.cpu_count,
        }


@dataclass
class QueryMetrics:
    """Database query metrics."""

    request_id: str
    query: str
    duration_ms: float
    timestamp: datetime
    connection_id: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "request_id": self.request_id,
            "query": self.query,
            "duration_ms": self.duration_ms,
            "timestamp": self.timestamp.isoformat(),
            "connection_id": self.connection_id,
        }

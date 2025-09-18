"""SQLite storage layer for TimeGlass profiling data."""

import sqlite3
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from .models import ProfilingMetrics, SystemMetrics, QueryMetrics


class TimeGlassStorage:
    """SQLite database storage for profiling data."""

    def __init__(self, db_path: str = "timeglass.db"):
        """Initialize database connection."""
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self):
        """Initialize database tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS profiling_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id TEXT UNIQUE NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    duration_ms REAL,
                    cpu_usage_percent REAL,
                    memory_usage_mb REAL,
                    memory_usage_percent REAL,
                    method TEXT,
                    path TEXT,
                    status_code INTEGER,
                    response_size_bytes INTEGER,
                    user_agent TEXT,
                    client_ip TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    cpu_usage_percent REAL NOT NULL,
                    memory_usage_mb REAL NOT NULL,
                    memory_usage_percent REAL NOT NULL,
                    total_memory_mb INTEGER NOT NULL,
                    cpu_count INTEGER NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS query_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id TEXT NOT NULL,
                    query TEXT NOT NULL,
                    duration_ms REAL NOT NULL,
                    timestamp TEXT NOT NULL,
                    connection_id TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (request_id) REFERENCES profiling_metrics (request_id)
                )
            """)

            # Create indexes for better query performance
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_profiling_request_id
                ON profiling_metrics (request_id)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_profiling_start_time
                ON profiling_metrics (start_time)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_system_timestamp
                ON system_metrics (timestamp)
            """)

            conn.commit()

    def save_profiling_metrics(self, metrics: ProfilingMetrics):
        """Save profiling metrics to database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO profiling_metrics (
                    request_id, start_time, end_time, duration_ms,
                    cpu_usage_percent, memory_usage_mb, memory_usage_percent,
                    method, path, status_code, response_size_bytes,
                    user_agent, client_ip
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                metrics.request_id,
                metrics.start_time.isoformat() if metrics.start_time else None,
                metrics.end_time.isoformat() if metrics.end_time else None,
                metrics.duration_ms,
                metrics.cpu_usage_percent,
                metrics.memory_usage_mb,
                metrics.memory_usage_percent,
                metrics.method,
                metrics.path,
                metrics.status_code,
                metrics.response_size_bytes,
                metrics.user_agent,
                metrics.client_ip,
            ))
            conn.commit()

    def save_system_metrics(self, metrics: SystemMetrics):
        """Save system metrics to database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO system_metrics (
                    timestamp, cpu_usage_percent, memory_usage_mb,
                    memory_usage_percent, total_memory_mb, cpu_count
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                metrics.timestamp.isoformat(),
                metrics.cpu_usage_percent,
                metrics.memory_usage_mb,
                metrics.memory_usage_percent,
                metrics.total_memory_mb,
                metrics.cpu_count,
            ))
            conn.commit()

    def save_query_metrics(self, metrics: QueryMetrics):
        """Save query metrics to database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO query_metrics (
                    request_id, query, duration_ms, timestamp, connection_id
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                metrics.request_id,
                metrics.query,
                metrics.duration_ms,
                metrics.timestamp.isoformat(),
                metrics.connection_id,
            ))
            conn.commit()

    def get_profiling_metrics(
        self,
        limit: int = 100,
        offset: int = 0,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[ProfilingMetrics]:
        """Get profiling metrics with optional filtering."""
        query = """
            SELECT request_id, start_time, end_time, duration_ms,
                   cpu_usage_percent, memory_usage_mb, memory_usage_percent,
                   method, path, status_code, response_size_bytes,
                   user_agent, client_ip
            FROM profiling_metrics
            WHERE 1=1
        """
        params = []

        if start_time:
            query += " AND start_time >= ?"
            params.append(start_time.isoformat())

        if end_time:
            query += " AND start_time <= ?"
            params.append(end_time.isoformat())

        query += " ORDER BY start_time DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()

        metrics = []
        for row in rows:
            data = {
                "request_id": row[0],
                "start_time": row[1],
                "end_time": row[2],
                "duration_ms": row[3],
                "cpu_usage_percent": row[4],
                "memory_usage_mb": row[5],
                "memory_usage_percent": row[6],
                "method": row[7],
                "path": row[8],
                "status_code": row[9],
                "response_size_bytes": row[10],
                "user_agent": row[11],
                "client_ip": row[12],
            }
            metrics.append(ProfilingMetrics.from_dict(data))

        return metrics

    def get_system_metrics(
        self,
        limit: int = 100,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[SystemMetrics]:
        """Get system metrics with optional time filtering."""
        query = """
            SELECT timestamp, cpu_usage_percent, memory_usage_mb,
                   memory_usage_percent, total_memory_mb, cpu_count
            FROM system_metrics
            WHERE 1=1
        """
        params = []

        if start_time:
            query += " AND timestamp >= ?"
            params.append(start_time.isoformat())

        if end_time:
            query += " AND timestamp <= ?"
            params.append(end_time.isoformat())

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()

        metrics = []
        for row in rows:
            metrics.append(SystemMetrics(
                timestamp=datetime.fromisoformat(row[0]),
                cpu_usage_percent=row[1],
                memory_usage_mb=row[2],
                memory_usage_percent=row[3],
                total_memory_mb=row[4],
                cpu_count=row[5],
            ))

        return metrics

    def get_stats_summary(self) -> dict:
        """Get summary statistics."""
        with sqlite3.connect(self.db_path) as conn:
            # Request statistics
            cursor = conn.execute("""
                SELECT
                    COUNT(*) as total_requests,
                    AVG(duration_ms) as avg_duration,
                    MAX(duration_ms) as max_duration,
                    MIN(duration_ms) as min_duration,
                    AVG(cpu_usage_percent) as avg_cpu,
                    AVG(memory_usage_percent) as avg_memory
                FROM profiling_metrics
                WHERE duration_ms IS NOT NULL
            """)
            req_stats = cursor.fetchone()

            # Recent system metrics
            cursor = conn.execute("""
                SELECT
                    AVG(cpu_usage_percent) as current_cpu,
                    AVG(memory_usage_percent) as current_memory
                FROM system_metrics
                WHERE timestamp >= datetime('now', '-1 hour')
            """)
            sys_stats = cursor.fetchone()

        return {
            "total_requests": req_stats[0] if req_stats[0] else 0,
            "avg_duration_ms": req_stats[1] if req_stats[1] else 0,
            "max_duration_ms": req_stats[2] if req_stats[2] else 0,
            "min_duration_ms": req_stats[3] if req_stats[3] else 0,
            "avg_cpu_percent": req_stats[4] if req_stats[4] else 0,
            "avg_memory_percent": req_stats[5] if req_stats[5] else 0,
            "current_cpu_percent": sys_stats[0] if sys_stats and sys_stats[0] else 0,
            "current_memory_percent": sys_stats[1] if sys_stats and sys_stats[1] else 0,
        }

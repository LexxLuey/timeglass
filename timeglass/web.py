"""TimeGlass web dashboard using FastAPI."""

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from datetime import datetime
import os
import logging

from .storage import TimeGlassStorage

# Setup logging
logger = logging.getLogger(__name__)


def create_app(db_path: str = "timeglass.db") -> FastAPI:
    """Create FastAPI application for TimeGlass dashboard."""
    app = FastAPI(
        title="TimeGlass Dashboard",
        description="Web dashboard for TimeGlass profiling data",
        version="0.1.0",
    )

    # Initialize storage
    storage = TimeGlassStorage(db_path)

    # Setup templates
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    templates = Jinja2Templates(directory=templates_dir)

    # Mount static files
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def dashboard(request: Request):
        """Main dashboard page."""
        try:
            return templates.TemplateResponse("dashboard.html", {"request": request})
        except Exception as e:
            logger.error(f"Error rendering dashboard: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @app.get("/api/stats")
    async def get_stats():
        """Get profiling statistics summary."""
        try:
            summary = storage.get_stats_summary()
            return JSONResponse(content=summary)
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve statistics")

    @app.get("/api/requests")
    async def get_requests(
        limit: int = Query(
            50, ge=1, le=1000, description="Number of requests to return"
        ),
        offset: int = Query(0, ge=0, description="Number of requests to skip"),
        start_time: Optional[datetime] = Query(
            None, description="Filter by start time (ISO format)"
        ),
        end_time: Optional[datetime] = Query(
            None, description="Filter by end time (ISO format)"
        ),
        method: Optional[str] = Query(None, description="Filter by HTTP method"),
        path_contains: Optional[str] = Query(
            None, description="Filter by path containing substring"
        ),
        status_code: Optional[int] = Query(
            None, description="Filter by HTTP status code"
        ),
    ):
        """Get profiling metrics with filtering."""
        try:
            # Validate parameters
            if limit > 1000:
                raise HTTPException(status_code=400, detail="Limit cannot exceed 1000")

            metrics = storage.get_profiling_metrics(
                limit=limit, offset=offset, start_time=start_time, end_time=end_time
            )

            # Apply additional filters in Python (could be optimized with SQL)
            if method:
                metrics = [m for m in metrics if m.method == method]
            if path_contains:
                metrics = [
                    m
                    for m in metrics
                    if path_contains.lower() in (m.path or "").lower()
                ]
            if status_code:
                metrics = [m for m in metrics if m.status_code == status_code]

            return JSONResponse(content=[m.to_dict() for m in metrics])
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting requests: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve requests")

    @app.get("/api/system-metrics")
    async def get_system_metrics(
        limit: int = Query(
            100, ge=1, le=1000, description="Number of metrics to return"
        ),
        start_time: Optional[datetime] = Query(
            None, description="Filter by start time (ISO format)"
        ),
        end_time: Optional[datetime] = Query(
            None, description="Filter by end time (ISO format)"
        ),
    ):
        """Get system metrics."""
        try:
            if limit > 1000:
                raise HTTPException(status_code=400, detail="Limit cannot exceed 1000")

            metrics = storage.get_system_metrics(
                limit=limit, start_time=start_time, end_time=end_time
            )
            return JSONResponse(content=[m.to_dict() for m in metrics])
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to retrieve system metrics"
            )

    @app.get("/request/{request_id}", response_class=HTMLResponse)
    async def request_detail(request_id: str, request: Request):
        """Detailed view for a specific request."""
        try:
            # Validate request_id format (basic check)
            if not request_id or len(request_id) > 100:
                raise HTTPException(status_code=400, detail="Invalid request ID")

            # Get the specific request
            metrics = storage.get_profiling_metrics(limit=1000)
            request_data = None
            for m in metrics:
                if m.request_id == request_id:
                    request_data = m
                    break

            if not request_data:
                logger.warning(f"Request {request_id} not found")
                raise HTTPException(status_code=404, detail="Request not found")

            logger.info(f"Found request {request_id}: method={request_data.method}, path={request_data.path}")

            # Determine status code class
            status_code = request_data.status_code
            if status_code and 200 <= status_code < 300:
                status_class = "2xx"
            elif status_code and 400 <= status_code < 500:
                status_class = "4xx"
            elif status_code and status_code >= 500:
                status_class = "5xx"
            else:
                status_class = "default"

            # Determine performance classes (same logic as dashboard)
            duration_ms = request_data.duration_ms
            if duration_ms is not None:
                if duration_ms < 100:
                    duration_class = "perf-good"
                elif duration_ms < 500:
                    duration_class = "perf-warning"
                else:
                    duration_class = "perf-critical"
            else:
                duration_class = "perf-neutral"

            cpu_percent = request_data.cpu_usage_percent
            if cpu_percent is not None:
                if cpu_percent < 50:
                    cpu_class = "perf-good"
                elif cpu_percent < 80:
                    cpu_class = "perf-warning"
                else:
                    cpu_class = "perf-critical"
            else:
                cpu_class = "perf-neutral"

            memory_percent = request_data.memory_usage_percent
            if memory_percent is not None:
                if memory_percent < 60:
                    memory_class = "perf-good"
                elif memory_percent < 85:
                    memory_class = "perf-warning"
                else:
                    memory_class = "perf-critical"
            else:
                memory_class = "perf-neutral"

            # Format data for template
            formatted_data = {
                "method": request_data.method or "N/A",
                "path": request_data.path or "N/A",
                "status_code": str(status_code) if status_code else "N/A",
                "status_class": status_class,
                "response_size_bytes": str(request_data.response_size_bytes) if request_data.response_size_bytes else "N/A",
                "user_agent": request_data.user_agent or "N/A",
                "client_ip": request_data.client_ip or "N/A",
                "start_time": request_data.start_time.isoformat() if request_data.start_time else "N/A",
                "end_time": request_data.end_time.isoformat() if request_data.end_time else "N/A",
                "duration": f"{request_data.duration_ms:.2f}ms" if request_data.duration_ms else "N/A",
                "duration_class": duration_class,
                "cpu_usage": f"{request_data.cpu_usage_percent:.1f}%" if request_data.cpu_usage_percent else "N/A",
                "cpu_class": cpu_class,
                "memory_usage": f"{request_data.memory_usage_mb:.2f} MB" if request_data.memory_usage_mb else "N/A",
                "memory_class": memory_class,
                "memory_percent": f"{request_data.memory_usage_percent:.1f}%" if request_data.memory_usage_percent else "N/A",
                "memory_percent_class": memory_class
            }

            logger.info(f"Formatted data for {request_id}: {formatted_data}")

            return templates.TemplateResponse(
                "request_detail.html", {
                    "request": request,
                    "request_id": request_id,
                    **formatted_data
                }
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error rendering request detail: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    return app


def start_dashboard(
    host: str = "127.0.0.1", port: int = 8000, db_path: str = "timeglass.db"
):
    """Start the TimeGlass dashboard server."""
    app = create_app(db_path)
    uvicorn.run(app, host=host, port=port)

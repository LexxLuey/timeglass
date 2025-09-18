"""TimeGlass FastAPI middleware for profiling."""

from typing import Callable
import time
import uuid
import json

# Import Rust functions if available
try:
    from . import start_profiling, stop_profiling, get_system_info
    _rust_available = True
except ImportError:
    _rust_available = False


class TimeGlassMiddleware:
    """Middleware for profiling FastAPI requests."""

    def __init__(self, app: Callable):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Generate unique request ID
        request_id = str(uuid.uuid4())

        # Start profiling with Rust extension
        try:
            if _rust_available:
                start_metrics_json = start_profiling(request_id)
                start_metrics = json.loads(start_metrics_json)
            else:
                raise Exception("Rust extension not available")
        except Exception as e:
            # Fallback to basic timing if Rust fails
            print(f"Failed to start Rust profiling: {e}")
            start_time = time.time()
            start_metrics = None

        # Process the request
        await self.app(scope, receive, send)

        # Stop profiling and collect metrics
        try:
            if start_metrics and _rust_available:
                final_metrics_json = stop_profiling(
                    request_id, start_metrics_json)
                final_metrics = json.loads(final_metrics_json)

                # Log the profiling results
                duration = final_metrics.get('duration_ms', 0)
                cpu_usage = final_metrics.get('cpu_usage_percent', 0)
                memory_mb = final_metrics.get('memory_usage_mb', 0)
                memory_percent = final_metrics.get('memory_usage_percent', 0)

                print(f"Request {request_id}: {duration:.2f}ms, "
                      f"CPU: {cpu_usage:.1f}%, "
                      f"Memory: {memory_mb:.1f}MB ({memory_percent:.1f}%)")
            else:
                # Fallback timing
                end_time = time.time()
                duration = (end_time - start_time) * 1000
                print(f"Request {request_id}: {duration:.2f}ms "
                      "(fallback timing)")
        except Exception as e:
            print(f"Failed to collect profiling metrics: {e}")

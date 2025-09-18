#!/usr/bin/env python3
"""Test FastAPI integration with TimeGlass middleware."""

import asyncio
import time
from fastapi import FastAPI
from timeglass import TimeGlassMiddleware
import uvicorn
import requests
import threading


def create_test_app():
    """Create a test FastAPI application."""
    app = FastAPI(title="TimeGlass Test API")

    # Add TimeGlass middleware
    app.add_middleware(TimeGlassMiddleware)

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {"message": "Hello World"}

    @app.get("/slow")
    async def slow_endpoint():
        """Slow endpoint for testing."""
        await asyncio.sleep(0.1)  # 100ms delay
        return {"message": "Slow response"}

    @app.get("/cpu-intensive")
    async def cpu_intensive():
        """CPU intensive endpoint."""
        # Simulate CPU work
        result = 0
        for i in range(100000):
            result += i * i
        return {"result": result}

    @app.get("/memory-test")
    async def memory_test():
        """Memory intensive endpoint."""
        # Create some memory usage
        data = [i for i in range(10000)]
        return {"data_length": len(data)}

    return app


def test_middleware():
    """Test the middleware by making requests."""
    print("🚀 Starting TimeGlass middleware integration test...")

    # Create test app
    app = create_test_app()

    # Start server in background thread
    def run_server():
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait for server to start
    time.sleep(2)

    try:
        print("📡 Making test requests...")

        # Test endpoints
        endpoints = [
            ("http://127.0.0.1:8000/", "Root endpoint"),
            ("http://127.0.0.1:8000/slow", "Slow endpoint"),
            ("http://127.0.0.1:8000/cpu-intensive", "CPU intensive"),
            ("http://127.0.0.1:8000/memory-test", "Memory test"),
        ]

        for url, description in endpoints:
            try:
                start_time = time.time()
                response = requests.get(url, timeout=10)
                end_time = time.time()

                print(f"✅ {description}: {response.status_code} "
                      f"({end_time - start_time:.3f}s)")

            except Exception as e:
                print(f"❌ {description}: Failed - {e}")

        print("\n🎯 Middleware integration test completed!")
        print("Check the server logs above for profiling metrics.")

    except Exception as e:
        print(f"❌ Test failed: {e}")

    finally:
        print("🛑 Stopping test server...")


if __name__ == "__main__":
    test_middleware()

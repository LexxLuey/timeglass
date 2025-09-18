"""TimeGlass - A lightweight profiling tool for FastAPI applications."""

__version__ = "0.1.0"

# Try to import the Rust extension
try:
    from .timeglass_core import (
        start_profiling, stop_profiling, get_system_info
    )
    _rust_available = True
except ImportError:
    _rust_available = False
    print("Warning: Rust extension not available, "
          "using fallback implementation")

from .middleware import TimeGlassMiddleware

__all__ = ["TimeGlassMiddleware"]

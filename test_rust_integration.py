#!/usr/bin/env python3
"""Test script to verify Rust extension integration."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import timeglass
    print("✓ Successfully imported timeglass package")

    # Test the functions directly from the package
    print("\nTesting Rust functions:")

    # Test start_profiling
    result = timeglass.start_profiling("test-request-123")
    print(f"start_profiling result: {result}")

    # Test stop_profiling
    final_result = timeglass.stop_profiling("test-request-123", result)
    print(f"stop_profiling result: {final_result}")

    # Test get_system_info
    system_info = timeglass.get_system_info()
    print(f"system_info: {system_info}")

    print("\n✓ All Rust functions working correctly!")

except ImportError as e:
    print(f"✗ Failed to import timeglass: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error testing Rust functions: {e}")
    sys.exit(1)

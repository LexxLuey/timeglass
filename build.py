#!/usr/bin/env python3
"""Build script for TimeGlass with Rust extension."""

import os
import subprocess
import sys
from pathlib import Path


def build_rust_extension():
    """Build the Rust extension using cargo."""
    print("Building Rust extension...")

    # Ensure we're in the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)

    # Build the Rust extension
    try:
        subprocess.run(
            ["cargo", "build", "--release"],
            check=True,
            capture_output=True,
            text=True
        )
        print("Rust extension built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to build Rust extension: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Cargo not found. Please install Rust and Cargo.")
        return False


def main():
    """Main build function."""
    if not build_rust_extension():
        sys.exit(1)

    print("Build completed successfully")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Setup script for TimeGlass with Rust extension."""

from setuptools import setup
from setuptools_rust import RustExtension


def main():
    """Main setup function."""
    setup(
        name="timeglass",
        version="0.1.0",
        description="A lightweight profiling tool for FastAPI applications",
        author="TimeGlass Team",
        author_email="team@timeglass.dev",
        license="MIT",
        packages=["timeglass"],
        rust_extensions=[
            RustExtension(
                "timeglass.timeglass_core",
                path="Cargo.toml",
                debug=False,
            )
        ],
        include_package_data=True,
        zip_safe=False,
    )


if __name__ == "__main__":
    main()

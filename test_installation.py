#!/usr/bin/env python3
"""
Quick test script to verify the seeed_mr60bha2 library is installed correctly.

Run this after installation to ensure everything is working.
"""

import sys


def test_import():
    """Test if the library can be imported."""
    print("Testing import...", end=" ")
    try:
        from seeed_mr60bha2 import SEEED_MR60BHA2
        print("✓ OK")
        return True
    except ImportError as e:
        print(f"✗ FAILED")
        print(f"  Error: {e}")
        print("\n  Solution: Install the package first:")
        print("    pip install -e .")
        return False


def test_dependencies():
    """Test if dependencies are installed."""
    print("Testing dependencies...", end=" ")
    try:
        import serial
        print("✓ OK")
        return True
    except ImportError:
        print("✗ FAILED")
        print("  Error: pyserial not installed")
        print("\n  Solution: Install dependencies:")
        print("    pip install pyserial")
        return False


def test_classes():
    """Test if classes are accessible."""
    print("Testing classes...", end=" ")
    try:
        from seeed_mr60bha2 import (
            SEEED_MR60BHA2,
            HeartBreathPhases,
            HeartBreathType,
            MmWaveError
        )
        print("✓ OK")
        return True
    except ImportError as e:
        print(f"✗ FAILED: {e}")
        return False


def test_version():
    """Test if version is accessible."""
    print("Testing version...", end=" ")
    try:
        from seeed_mr60bha2 import __version__
        print(f"✓ OK (v{__version__})")
        return True
    except ImportError:
        print("✗ WARNING (version not found)")
        return True  # Not critical


def print_system_info():
    """Print system information."""
    print("\nSystem Information:")
    print(f"  Python: {sys.version}")
    print(f"  Platform: {sys.platform}")

    try:
        import serial
        print(f"  pyserial: {serial.__version__}")
    except:
        print("  pyserial: Not installed")


def main():
    """Run all tests."""
    print("=" * 60)
    print(" Testing seeed_mr60bha2 Installation")
    print("=" * 60)
    print()

    tests = [
        test_dependencies,
        test_import,
        test_classes,
        test_version,
    ]

    results = [test() for test in tests]

    print_system_info()

    print("\n" + "=" * 60)
    if all(results):
        print("✓ All tests passed! Installation is successful.")
        print("\nNext steps:")
        print("  1. Find your serial port:")
        print("     python examples/port_detector.py --list")
        print("  2. Run an example:")
        print("     python examples/basic_usage.py")
        print("=" * 60)
        return 0
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())

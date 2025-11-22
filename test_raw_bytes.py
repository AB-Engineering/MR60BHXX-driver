#!/usr/bin/env python3
"""
Test script to capture and display raw bytes from the sensor.
Run this to help debug data parsing issues.
"""

import sys
import time
import struct
from seeed_mr60bha2 import SEEED_MR60BHA2


def test_float_conversion(raw_bytes):
    """Test different ways to convert bytes to float."""
    if len(raw_bytes) < 4:
        return

    print(f"  Raw bytes: {raw_bytes.hex(' ')}")
    print(f"  As little-endian float: {struct.unpack('<f', raw_bytes)[0]:.4f}")
    print(f"  As big-endian float: {struct.unpack('>f', raw_bytes)[0]:.4f}")
    print(f"  Raw as integers: {[b for b in raw_bytes]}")


def main():
    # CHANGE THIS TO YOUR PORT!
    SERIAL_PORT = '/dev/serial0'  # or '/dev/cu.usbserial-*' on macOS

    print("="*70)
    print(" MR60BHA2 Raw Data Debug Test")
    print("="*70)
    print(f"\nConnecting to {SERIAL_PORT}...")

    # Enable debug mode to see raw data
    sensor = SEEED_MR60BHA2(SERIAL_PORT, debug=True)

    try:
        sensor.begin()
        print("✓ Connected!\n")
        print("Collecting data for 10 seconds...")
        print("Position yourself 25-50cm from the sensor\n")

        start_time = time.time()
        while time.time() - start_time < 10:
            if sensor.update(timeout=0.1):
                pass  # Debug output will show automatically

            time.sleep(0.1)

        print("\n" + "="*70)
        print("Test complete! Please share the debug output above.")
        print("="*70)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        sensor.close()

    return 0


if __name__ == '__main__':
    sys.exit(main())

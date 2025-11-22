#!/usr/bin/env python3
"""
Debug script to see raw frame data from the sensor.

This helps diagnose data parsing issues.
"""

import time
import sys
import struct
from seeed_mr60bha2 import SEEED_MR60BHA2


def parse_float_both_ways(data):
    """Parse float as both little and big endian to debug."""
    if len(data) < 4:
        return None, None

    little = struct.unpack('<f', data[:4])[0]
    big = struct.unpack('>f', data[:4])[0]

    return little, big


def main():
    # Change this to your port
    SERIAL_PORT = '/dev/serial0'

    sensor = SEEED_MR60BHA2(SERIAL_PORT, debug=True)

    try:
        sensor.begin()
        print("Connected! Watching raw data...\n")

        count = 0
        while count < 20:  # Just capture 20 frames
            if sensor.update(timeout=0.1):
                data = sensor.get_all_data()

                # Check distance data
                if data['distance_valid']:
                    print(f"\nFrame {count}:")
                    print(f"  Distance: {data['distance']:.2f}m")
                    print(f"  Range Flag: {sensor._range_flag}")

                    # Try to show raw bytes if possible
                    # This would require modifying the library temporarily

                    count += 1

                # Check heart rate
                if data['heart_rate_valid']:
                    print(f"  Heart Rate: {data['heart_rate']:.2f} BPM")

                # Check breath rate
                if data['breath_rate_valid']:
                    print(f"  Breath Rate: {data['breath_rate']:.2f} BPM")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopped")
    finally:
        sensor.close()


if __name__ == '__main__':
    sys.exit(main())

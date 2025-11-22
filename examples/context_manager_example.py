#!/usr/bin/env python3
"""
Example using context manager for automatic resource cleanup.

This example demonstrates the use of Python's context manager protocol
to ensure the serial connection is properly closed.

Author: AB-Engineering
Date: 2025-11-22
"""

import time
import sys
from seeed_mr60bha2 import SEEED_MR60BHA2


def main():
    # Use context manager for automatic cleanup
    with SEEED_MR60BHA2('/dev/serial0', debug=True) as sensor:
        print("Connected to sensor!")
        print("Waiting for heart rate data...\n")

        # Wait for specific measurements
        heart_rate = sensor.wait_for_heart_rate(timeout=10.0)
        if heart_rate is not None:
            print(f"Heart Rate: {heart_rate:.2f} BPM")
        else:
            print("No heart rate data received within timeout")

        breath_rate = sensor.wait_for_breath_rate(timeout=10.0)
        if breath_rate is not None:
            print(f"Breath Rate: {breath_rate:.2f} BPM")
        else:
            print("No breath rate data received within timeout")

        distance = sensor.wait_for_distance(timeout=10.0)
        if distance is not None:
            print(f"Distance: {distance:.2f} m")
        else:
            print("No distance data received within timeout")

    # Sensor is automatically closed when exiting the 'with' block
    print("\nSensor connection automatically closed")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

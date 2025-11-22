#!/usr/bin/env python3
"""
Basic usage example for the Seeed MR60BHA2 mmWave sensor.

This example demonstrates how to read heart rate and breath rate
from the sensor on a Raspberry Pi.

Author: AB-Engineering
Date: 2025-01-22
"""

import time
import sys
from seeed_mr60bha2 import SEEED_MR60BHA2


def main():
    # Initialize the sensor on Raspberry Pi UART port
    # Common ports: '/dev/serial0', '/dev/ttyAMA0', '/dev/ttyUSB0'
    sensor = SEEED_MR60BHA2(
        port='/dev/serial0',  # Change this to match your setup
        baud_rate=115200,
        debug=False  # Set to True for debug output
    )

    try:
        # Connect to the sensor
        print("Connecting to MR60BHA2 sensor...")
        sensor.begin()
        print("Connected successfully!")
        print("\nStarting heart rate and breath rate monitoring...")
        print("Place your hand or body in front of the sensor (0.5-1.5m distance)")
        print("\nNote: Breath rate may take 1-2 minutes to appear after heart rate.")
        print("Stay very still and breathe normally for best results.")
        print("-" * 60)

        # Main loop
        while True:
            # Update sensor - fetch and process new data
            if sensor.update(timeout=0.1):
                # Try to get heart rate
                heart_rate = sensor.get_heart_rate()
                if heart_rate is not None:
                    print(f"Heart Rate: {heart_rate:6.2f} BPM", end="  ")

                # Try to get breath rate
                breath_rate = sensor.get_breath_rate()
                if breath_rate is not None and breath_rate > 0:
                    print(f"Breath Rate: {breath_rate:6.2f} BPM", end="  ")

                # Try to get distance
                distance = sensor.get_distance()
                if distance is not None:
                    print(f"Distance: {distance:5.2f}m", end="  ")

                # Try to get phase data
                phases = sensor.get_heart_breath_phases()
                if phases is not None:
                    print(f"Phases: T={phases.total_phase:.2f} "
                          f"B={phases.breath_phase:.2f} "
                          f"H={phases.heart_phase:.2f}", end="")

                # Print newline if any data was received
                if any([heart_rate, breath_rate, distance, phases]):
                    print()

            # Small delay to prevent excessive CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n\nStopping monitoring...")
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1
    finally:
        # Clean up
        sensor.close()
        print("Sensor connection closed")

    return 0


if __name__ == '__main__':
    sys.exit(main())

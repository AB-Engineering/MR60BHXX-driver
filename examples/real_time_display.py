#!/usr/bin/env python3
"""
Real-time display with formatted output.

This example demonstrates real-time monitoring with a formatted display
that updates in place.

Author: AB-Engineering
Date: 2025-11-22
"""

import time
import sys
from datetime import datetime
from seeed_mr60bha2 import SEEED_MR60BHA2


def clear_lines(n):
    """Clear n lines from terminal."""
    for _ in range(n):
        sys.stdout.write('\033[F')  # Move cursor up
        sys.stdout.write('\033[K')  # Clear line


def format_value(value, unit, width=10):
    """Format a value with unit or show 'N/A'."""
    if value is not None:
        return f"{value:{width}.2f} {unit}"
    else:
        return f"{'N/A':>{width+len(unit)+1}}"


def main():
    sensor = SEEED_MR60BHA2(
        port='/dev/serial0',
        baud_rate=115200,
        debug=False
    )

    try:
        print("Connecting to MR60BHA2 sensor...")
        sensor.begin()
        print("Connected successfully!\n")
        time.sleep(1)

        # Print initial display
        lines_to_clear = 0

        while True:
            # Update sensor
            sensor.update(timeout=0.1)

            # Get all data (non-consuming)
            data = sensor.get_all_data()

            # Clear previous display
            if lines_to_clear > 0:
                clear_lines(lines_to_clear)

            # Build display
            display = []
            display.append("=" * 70)
            display.append(f"  MR60BHA2 mmWave Sensor Monitor - {datetime.now().strftime('%H:%M:%S')}")
            display.append("=" * 70)
            display.append("")

            # Heart Rate
            hr_value = data['heart_rate'] if data['heart_rate_valid'] else None
            display.append(f"  ❤️  Heart Rate:   {format_value(hr_value, 'BPM')}")

            # Breath Rate
            br_value = data['breath_rate'] if data['breath_rate_valid'] else None
            display.append(f"  🫁  Breath Rate:  {format_value(br_value, 'BPM')}")

            # Distance
            dist_value = data['distance'] if data['distance_valid'] else None
            display.append(f"  📏  Distance:     {format_value(dist_value, 'm  ')}")

            display.append("")

            # Phase information
            if data['phases_valid']:
                phases = data['phases']
                display.append("  Phase Information:")
                display.append(f"    Total Phase:  {phases.total_phase:10.2f}")
                display.append(f"    Breath Phase: {phases.breath_phase:10.2f}")
                display.append(f"    Heart Phase:  {phases.heart_phase:10.2f}")
            else:
                display.append("  Phase Information: N/A")

            display.append("")
            display.append("  Press Ctrl+C to stop")
            display.append("=" * 70)

            # Print display
            output = '\n'.join(display)
            print(output)
            lines_to_clear = len(display)

            time.sleep(0.5)

    except KeyboardInterrupt:
        if lines_to_clear > 0:
            clear_lines(lines_to_clear)
        print("\nStopping monitoring...")
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1
    finally:
        sensor.close()
        print("Sensor connection closed")

    return 0


if __name__ == '__main__':
    sys.exit(main())

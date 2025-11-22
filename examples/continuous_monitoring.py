#!/usr/bin/env python3
"""
Continuous monitoring example with CSV logging.

This example demonstrates continuous monitoring with data logging to a CSV file.

Author: AB-Engineering
Date: 2025-11-22
"""

import time
import sys
import csv
from datetime import datetime
from pathlib import Path
from seeed_mr60bha2 import SEEED_MR60BHA2


def main():
    # Initialize the sensor
    sensor = SEEED_MR60BHA2(
        port='/dev/serial0',
        baud_rate=115200,
        debug=False
    )

    # Setup CSV logging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = Path(f"sensor_data_{timestamp}.csv")

    try:
        # Connect to the sensor
        print("Connecting to MR60BHA2 sensor...")
        sensor.begin()
        print("Connected successfully!")
        print(f"\nLogging data to: {csv_file}")
        print("Press Ctrl+C to stop monitoring")
        print("-" * 80)

        # Open CSV file for writing
        with open(csv_file, 'w', newline='') as f:
            csv_writer = csv.writer(f)
            # Write header
            csv_writer.writerow([
                'Timestamp',
                'Heart_Rate_BPM',
                'Breath_Rate_BPM',
                'Distance_m',
                'Total_Phase',
                'Breath_Phase',
                'Heart_Phase'
            ])

            # Main monitoring loop
            sample_count = 0
            while True:
                # Update sensor
                if sensor.update(timeout=0.1):
                    # Get all current data
                    data = sensor.get_all_data()

                    # Prepare row data
                    timestamp = datetime.now().isoformat()
                    row = [
                        timestamp,
                        data['heart_rate'] if data['heart_rate_valid'] else '',
                        data['breath_rate'] if data['breath_rate_valid'] else '',
                        data['distance'] if data['distance_valid'] else '',
                        data['phases'].total_phase if data['phases_valid'] else '',
                        data['phases'].breath_phase if data['phases_valid'] else '',
                        data['phases'].heart_phase if data['phases_valid'] else '',
                    ]

                    # Write to CSV
                    csv_writer.writerow(row)
                    f.flush()  # Ensure data is written immediately

                    sample_count += 1

                    # Print status every 10 samples
                    if sample_count % 10 == 0:
                        print(f"Samples logged: {sample_count}", end='\r')

                time.sleep(0.1)

    except KeyboardInterrupt:
        print(f"\n\nStopping monitoring. Total samples: {sample_count}")
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1
    finally:
        sensor.close()
        print("Sensor connection closed")

    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""
Focused test to capture and analyze breath rate frames specifically.
"""

import sys
import time
from seeed_mr60bha2 import SEEED_MR60BHA2

def main():
    SERIAL_PORT = '/dev/serial0'  # Change this to match your setup

    print("="*70)
    print(" Breath Rate Frame Analysis")
    print("="*70)
    print(f"\nConnecting to {SERIAL_PORT}...")

    sensor = SEEED_MR60BHA2(SERIAL_PORT, debug=True)

    try:
        sensor.begin()
        print("✓ Connected!\n")
        print("Monitoring breath rate frames for 30 seconds...")
        print("Stay VERY still and breathe normally\n")
        print("-" * 70)

        breath_rate_count = 0
        non_zero_count = 0
        start_time = time.time()

        while time.time() - start_time < 30:
            if sensor.update(timeout=0.1):
                # Check specifically for breath rate
                breath_rate = sensor.get_breath_rate()
                if breath_rate is not None:
                    breath_rate_count += 1
                    status = "✓ DETECTED" if breath_rate > 0 else "✗ Zero"
                    if breath_rate > 0:
                        non_zero_count += 1
                    print(f"[{breath_rate_count:3d}] Breath Rate: {breath_rate:6.2f} BPM  {status}")

            time.sleep(0.1)

        print("\n" + "="*70)
        print("SUMMARY:")
        print(f"  Total breath rate frames received: {breath_rate_count}")
        print(f"  Non-zero readings: {non_zero_count}")
        print(f"  Zero readings: {breath_rate_count - non_zero_count}")

        if breath_rate_count > 0:
            detection_rate = (non_zero_count / breath_rate_count) * 100
            print(f"  Detection rate: {detection_rate:.1f}%")

        print("\nNOTE: Zero readings mean the sensor hasn't locked onto your")
        print("breath pattern yet. This is normal sensor behavior, NOT a")
        print("parsing issue. The sensor needs:")
        print("  - You to be completely still")
        print("  - Normal breathing (not too deep, not holding breath)")
        print("  - 10-60 seconds to establish a stable breath rate lock")
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

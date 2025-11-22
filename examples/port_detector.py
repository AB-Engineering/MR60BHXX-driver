#!/usr/bin/env python3
"""
Serial port detection utility for MR60BHA2 sensor.

This script helps you find and test the correct serial port
for your MR60BHA2 sensor on any platform (macOS, Linux, Windows).

Author: AB-Engineering
Date: 2025-11-22
"""

import sys
import time
import serial.tools.list_ports
from seeed_mr60bha2 import SEEED_MR60BHA2


def list_serial_ports():
    """List all available serial ports."""
    ports = serial.tools.list_ports.comports()

    if not ports:
        print("❌ No serial ports found!")
        print("\nTroubleshooting:")
        print("  - Make sure your USB-to-Serial adapter is connected")
        print("  - Check if drivers are installed (Windows/macOS)")
        print("  - On Raspberry Pi, ensure UART is enabled")
        return []

    print("Available serial ports:\n")
    for i, port in enumerate(ports):
        print(f"  [{i}] {port.device}")
        print(f"      Description: {port.description}")
        print(f"      Hardware ID: {port.hwid}")
        print()

    return ports


def test_sensor_connection(port, timeout=5.0):
    """Test connection to sensor on specified port."""
    print(f"\n{'='*60}")
    print(f"Testing port: {port}")
    print(f"{'='*60}\n")

    try:
        # Try to open connection
        print("1. Opening serial connection...", end=' ')
        sensor = SEEED_MR60BHA2(port, debug=False)
        sensor.begin()
        print("✓ OK")

        # Try to receive data
        print("2. Waiting for sensor data...", end=' ')
        sys.stdout.flush()

        start_time = time.time()
        data_received = False

        while time.time() - start_time < timeout:
            if sensor.update(timeout=0.1):
                data = sensor.get_all_data()
                if any([data['heart_rate_valid'], data['breath_rate_valid'],
                       data['distance_valid'], data['phases_valid']]):
                    data_received = True
                    print("✓ OK")
                    print("\n3. Data received:")
                    if data['heart_rate_valid']:
                        print(f"   Heart Rate: {data['heart_rate']:.2f} BPM")
                    if data['breath_rate_valid']:
                        print(f"   Breath Rate: {data['breath_rate']:.2f} BPM")
                    if data['distance_valid']:
                        print(f"   Distance: {data['distance']:.2f} m")
                    break
            time.sleep(0.1)

        if not data_received:
            print("⚠ TIMEOUT")
            print("\n   No data received. This could mean:")
            print("   - Sensor is not connected to this port")
            print("   - Sensor is not powered")
            print("   - Wrong baud rate (should be 115200)")
            print("   - No person detected in range")

        sensor.close()
        print("\n4. Connection test complete!")
        return data_received

    except PermissionError:
        print("❌ PERMISSION DENIED")
        print("\n   Solution:")
        print("   - Linux/macOS: Add user to dialout group")
        print("     sudo usermod -a -G dialout $USER")
        print("     (then log out and back in)")
        print("   - Windows: Run as administrator")
        return False

    except Exception as e:
        print(f"❌ ERROR")
        print(f"\n   {type(e).__name__}: {e}")
        return False


def interactive_mode():
    """Interactive mode to select and test ports."""
    print("=" * 60)
    print(" MR60BHA2 Sensor - Serial Port Detector")
    print("=" * 60)
    print()

    # List all ports
    ports = list_serial_ports()
    if not ports:
        return 1

    # User selection
    while True:
        try:
            choice = input(f"Select port to test (0-{len(ports)-1}, 'a' for all, 'q' to quit): ").strip().lower()

            if choice == 'q':
                print("Exiting...")
                return 0

            if choice == 'a':
                # Test all ports
                print("\nTesting all ports...\n")
                for port in ports:
                    test_sensor_connection(port.device, timeout=3.0)
                    time.sleep(1)
                return 0

            # Test specific port
            port_index = int(choice)
            if 0 <= port_index < len(ports):
                result = test_sensor_connection(ports[port_index].device, timeout=5.0)
                if result:
                    print("\n" + "="*60)
                    print("✓ SUCCESS! Use this port in your code:")
                    print(f"\n  sensor = SEEED_MR60BHA2('{ports[port_index].device}')")
                    print("="*60)
                return 0
            else:
                print(f"Invalid selection. Please enter 0-{len(ports)-1}")

        except ValueError:
            print("Invalid input. Please enter a number, 'a', or 'q'")
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
            return 1


def auto_detect_mode():
    """Automatically detect the sensor port."""
    print("Auto-detecting MR60BHA2 sensor...\n")

    ports = serial.tools.list_ports.comports()
    if not ports:
        print("❌ No serial ports found!")
        return None

    for port in ports:
        print(f"Testing {port.device}...", end=' ')
        sys.stdout.flush()

        try:
            sensor = SEEED_MR60BHA2(port.device, debug=False)
            sensor.begin()

            # Quick test
            found = False
            for _ in range(10):
                if sensor.update(timeout=0.1):
                    found = True
                    break
                time.sleep(0.1)

            sensor.close()

            if found:
                print("✓ FOUND!")
                return port.device
            else:
                print("✗")

        except:
            print("✗")

    return None


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--auto':
            # Auto-detect mode
            port = auto_detect_mode()
            if port:
                print(f"\n✓ Sensor found on: {port}")
                print(f"\nUse this in your code:")
                print(f"  sensor = SEEED_MR60BHA2('{port}')")
                return 0
            else:
                print("\n❌ Sensor not found on any port")
                return 1
        elif sys.argv[1] == '--list':
            # Just list ports
            list_serial_ports()
            return 0
        else:
            # Test specific port
            return 0 if test_sensor_connection(sys.argv[1]) else 1
    else:
        # Interactive mode
        return interactive_mode()


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)

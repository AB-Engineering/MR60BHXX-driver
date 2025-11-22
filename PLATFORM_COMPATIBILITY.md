# Platform Compatibility Guide

The Seeed MR60BHA2 Python library is **cross-platform** and works on any system that supports Python and serial communication.

## Supported Platforms

### ✅ Linux (Raspberry Pi, Ubuntu, Debian, etc.)
- **Serial Ports**: `/dev/ttyUSB0`, `/dev/ttyACM0`, `/dev/serial0`, `/dev/ttyAMA0`
- **Setup**: May need to add user to `dialout` group
- **Works**: Yes, fully tested

### ✅ macOS
- **Serial Ports**: `/dev/cu.usbserial-*`, `/dev/tty.usbserial-*`
- **Setup**: No special permissions needed (usually)
- **Works**: Yes, fully compatible

### ✅ Windows
- **Serial Ports**: `COM1`, `COM2`, `COM3`, etc.
- **Setup**: Install pyserial (automatically handled by pip)
- **Works**: Yes, fully compatible

## Usage on Different Platforms

### Raspberry Pi (Default Examples)
```python
from seeed_mr60bha2 import SEEED_MR60BHA2

# Using built-in UART
sensor = SEEED_MR60BHA2('/dev/serial0')
sensor.begin()
```

### macOS
```python
from seeed_mr60bha2 import SEEED_MR60BHA2

# Using USB-to-Serial adapter
sensor = SEEED_MR60BHA2('/dev/cu.usbserial-A50285BI')
# or
sensor = SEEED_MR60BHA2('/dev/tty.usbserial-A50285BI')
sensor.begin()
```

### Windows
```python
from seeed_mr60bha2 import SEEED_MR60BHA2

# Using COM port
sensor = SEEED_MR60BHA2('COM3')
sensor.begin()
```

### Linux (Desktop/Laptop with USB-to-Serial)
```python
from seeed_mr60bha2 import SEEED_MR60BHA2

# Using USB-to-Serial adapter
sensor = SEEED_MR60BHA2('/dev/ttyUSB0')
sensor.begin()
```

## Finding Your Serial Port

### macOS
```bash
# List all serial devices
ls /dev/cu.*
ls /dev/tty.*

# Or use:
python -m serial.tools.list_ports
```

### Linux
```bash
# List all serial devices
ls /dev/tty*

# Or use:
python -m serial.tools.list_ports

# Check device permissions
ls -l /dev/ttyUSB0
```

### Windows
```powershell
# List COM ports in Device Manager
# Or in Python:
python -m serial.tools.list_ports
```

## Python Script to Auto-Detect Port

```python
#!/usr/bin/env python3
"""Auto-detect serial port for MR60BHA2 sensor."""

import serial.tools.list_ports
from seeed_mr60bha2 import SEEED_MR60BHA2

def find_serial_port():
    """Find available serial ports."""
    ports = serial.tools.list_ports.comports()
    print("Available serial ports:")
    for i, port in enumerate(ports):
        print(f"{i}: {port.device} - {port.description}")

    if not ports:
        print("No serial ports found!")
        return None

    # Auto-select first port or let user choose
    if len(ports) == 1:
        return ports[0].device
    else:
        choice = input(f"Select port (0-{len(ports)-1}): ")
        return ports[int(choice)].device

# Use it
port = find_serial_port()
if port:
    print(f"\nUsing port: {port}")
    sensor = SEEED_MR60BHA2(port)
    sensor.begin()
    print("Connected successfully!")
    sensor.close()
```

## Connection Methods by Platform

### Raspberry Pi
- **Direct UART** (recommended): Connect sensor directly to GPIO pins
- **USB-to-Serial**: Use any USB-to-TTL adapter

### macOS / Windows / Linux Desktop
- **USB-to-Serial Adapter** (required): You need a USB-to-TTL adapter
  - Common chips: CP2102, CH340, FT232, PL2303
  - Connect sensor TX → Adapter RX, sensor RX → Adapter TX
  - Power sensor separately (5V)

## Hardware Connections

### Using USB-to-Serial Adapter (All Platforms)

| MR60BHA2 | USB-to-TTL Adapter |
|----------|--------------------|
| VCC      | 5V (or external)   |
| GND      | GND                |
| TX       | RX                 |
| RX       | TX                 |

**Important**: Some USB-to-Serial adapters don't provide 5V power. You may need to power the sensor separately.

### Raspberry Pi Direct Connection

| MR60BHA2 | Raspberry Pi |
|----------|--------------|
| VCC      | 5V (Pin 2)   |
| GND      | GND (Pin 6)  |
| TX       | RX (Pin 10)  |
| RX       | TX (Pin 8)   |

## Platform-Specific Notes

### Raspberry Pi
- Enable UART: `sudo raspi-config` → Interface Options → Serial
- Disable login shell on serial
- Add user to dialout group: `sudo usermod -a -G dialout $USER`

### macOS
- Usually works out of the box with USB-to-Serial adapters
- Install driver if needed (CH340, CP2102 drivers from manufacturer)
- Both `/dev/cu.*` and `/dev/tty.*` work, but `cu` is preferred for output

### Windows
- Install USB-to-Serial driver from manufacturer
- Check COM port number in Device Manager
- No special permissions needed

### Linux Desktop/Laptop
- Add user to dialout group: `sudo usermod -a -G dialout $USER`
- May need to install USB-to-Serial driver (usually built into kernel)
- Log out and back in after adding to dialout group

## Testing Your Setup

```python
#!/usr/bin/env python3
"""Test serial connection to MR60BHA2."""

import sys
from seeed_mr60bha2 import SEEED_MR60BHA2

# Change this to match your platform
SERIAL_PORT = '/dev/serial0'  # Raspberry Pi
# SERIAL_PORT = '/dev/cu.usbserial-A50285BI'  # macOS
# SERIAL_PORT = 'COM3'  # Windows
# SERIAL_PORT = '/dev/ttyUSB0'  # Linux with USB adapter

def test_sensor(port):
    try:
        print(f"Testing connection to {port}...")
        sensor = SEEED_MR60BHA2(port, debug=True)
        sensor.begin()
        print("✓ Connection successful!")

        print("\nWaiting for data (10 seconds)...")
        import time
        for i in range(100):
            if sensor.update(timeout=0.1):
                print("✓ Data received!")
                data = sensor.get_all_data()
                print(f"  Heart Rate Valid: {data['heart_rate_valid']}")
                print(f"  Breath Rate Valid: {data['breath_rate_valid']}")
                break
            time.sleep(0.1)
        else:
            print("⚠ No data received (sensor may need time to stabilize)")

        sensor.close()
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    success = test_sensor(SERIAL_PORT)
    sys.exit(0 if success else 1)
```

## Summary

**The library is completely cross-platform!** The only difference is the serial port name you use:

- **Raspberry Pi**: `/dev/serial0`, `/dev/ttyAMA0`
- **macOS**: `/dev/cu.usbserial-*`
- **Windows**: `COM3`, `COM4`, etc.
- **Linux**: `/dev/ttyUSB0`, `/dev/ttyACM0`

Everything else in the library is pure Python and works identically across all platforms.

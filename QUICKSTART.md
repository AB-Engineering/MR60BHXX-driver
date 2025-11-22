# Quick Start Guide

Get up and running with the MR60BHA2 sensor in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install pyserial
```

## Step 2: Install the Library

```bash
cd mmWave-python
pip install -e .
```

## Step 3: Find Your Serial Port

Run the port detector:
```bash
python examples/port_detector.py
```

This will show you all available serial ports and let you test them.

**Common ports by platform:**
- Raspberry Pi: `/dev/serial0` or `/dev/ttyAMA0`
- macOS: `/dev/cu.usbserial-*`
- Linux: `/dev/ttyUSB0`
- Windows: `COM3`, `COM4`, etc.

## Step 4: Test the Connection

Create a file `test.py`:

```python
from seeed_mr60bha2 import SEEED_MR60BHA2
import time

# Change this to your port!
SERIAL_PORT = '/dev/serial0'  # or COM3, /dev/cu.usbserial-*, etc.

sensor = SEEED_MR60BHA2(SERIAL_PORT, debug=True)
sensor.begin()

print("Sensor connected! Waiting for data...")
print("Position yourself 0.5-1.5m in front of the sensor\n")

try:
    while True:
        if sensor.update():
            heart_rate = sensor.get_heart_rate()
            breath_rate = sensor.get_breath_rate()

            if heart_rate:
                print(f"❤️  Heart Rate: {heart_rate:.1f} BPM")
            if breath_rate:
                print(f"🫁 Breath Rate: {breath_rate:.1f} BPM")

        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped")
finally:
    sensor.close()
```

Run it:
```bash
python test.py
```

## Step 5: Use in Your Project

```python
from seeed_mr60bha2 import SEEED_MR60BHA2

# Simple usage with context manager
with SEEED_MR60BHA2('/dev/serial0') as sensor:
    while True:
        if sensor.update():
            data = sensor.get_all_data()

            if data['heart_rate_valid']:
                print(f"Heart: {data['heart_rate']:.1f} BPM")

            if data['breath_rate_valid']:
                print(f"Breath: {data['breath_rate']:.1f} BPM")
```

## Troubleshooting

### "Permission denied" error
**Linux/Raspberry Pi:**
```bash
sudo usermod -a -G dialout $USER
# Log out and back in
```

### No data received
1. Check connections (TX → RX, RX → TX)
2. Ensure sensor is powered (5V)
3. Stand 0.5-1.5m in front of sensor
4. Wait a few seconds for sensor to stabilize

### Wrong serial port
Use the port detector:
```bash
python examples/port_detector.py --auto
```

## Next Steps

- Check out more examples in the `examples/` directory
- Read the full [README.md](README.md) for API reference
- See [PLATFORM_COMPATIBILITY.md](PLATFORM_COMPATIBILITY.md) for platform-specific tips

## Working Examples

All example scripts are ready to run:

```bash
# Basic monitoring
python examples/basic_usage.py

# CSV logging
python examples/continuous_monitoring.py

# Real-time formatted display
python examples/real_time_display.py

# Using context managers
python examples/context_manager_example.py
```

Just change the `SERIAL_PORT` variable in each file to match your system!

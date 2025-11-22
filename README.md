# Seeed MR60BHA2 mmWave Sensor - Python Library

A complete, **cross-platform** Python library for interfacing with the Seeed MR60BHA2 mmWave heart rate and breath monitoring sensor.

## Features

- **Pure Python Implementation**: 100% Python-compliant code using standard libraries
- **Cross-Platform**: Works on Raspberry Pi, macOS, Linux, and Windows
- **Easy to Use**: Simple API for reading heart rate and breath rate data
- **Robust Communication**: Automatic frame parsing, checksum validation, and error handling
- **Flexible**: Support for both polling and event-driven data collection
- **Well Documented**: Comprehensive documentation and examples
- **Production Ready**: Proper logging, error handling, and resource management
- **Context Manager Support**: Automatic resource cleanup using Python's `with` statement

## Platform Support

- ✅ **Raspberry Pi** - Direct UART connection or USB-to-Serial
- ✅ **macOS** - USB-to-Serial adapter
- ✅ **Linux** (Desktop/Server) - USB-to-Serial adapter
- ✅ **Windows** - USB-to-Serial adapter

See [PLATFORM_COMPATIBILITY.md](PLATFORM_COMPATIBILITY.md) for detailed platform-specific instructions.

## Hardware Requirements

- Seeed MR60BHA2 mmWave Sensor
- **Raspberry Pi**: Direct UART connection (GPIO pins)
- **Other Platforms**: USB-to-Serial adapter (CP2102, CH340, FT232, etc.)

## Installation

### Prerequisites

**All Platforms:**
```bash
pip install pyserial
```

**Raspberry Pi Only** (if using direct UART):
```bash
sudo raspi-config
# Navigate to: Interface Options -> Serial Port
# - Login shell over serial: NO
# - Serial port hardware enabled: YES
```

### Install the Library

```bash
# Clone the repository
git clone <repository-url>
cd mmWave-python

# Create and activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Or install directly
pip install .
```

**Having trouble?** See the detailed [INSTALL.md](INSTALL.md) guide.

### Finding Your Serial Port

Use the included port detector utility:
```bash
# Interactive mode - helps you find and test ports
python examples/port_detector.py

# Auto-detect mode
python examples/port_detector.py --auto

# List all available ports
python examples/port_detector.py --list
```

## Quick Start

```python
from seeed_mr60bha2 import SEEED_MR60BHA2
import time

# Initialize sensor
sensor = SEEED_MR60BHA2('/dev/serial0')
sensor.begin()

# Read data
while True:
    if sensor.update():
        heart_rate = sensor.get_heart_rate()
        breath_rate = sensor.get_breath_rate()

        if heart_rate:
            print(f"Heart Rate: {heart_rate} BPM")
        if breath_rate:
            print(f"Breath Rate: {breath_rate} BPM")

    time.sleep(0.1)
```

## Wiring

Connect the MR60BHA2 sensor to your Raspberry Pi:

| MR60BHA2 | Raspberry Pi |
|----------|--------------|
| VCC      | 5V (Pin 2)   |
| GND      | GND (Pin 6)  |
| TX       | RX (Pin 10)  |
| RX       | TX (Pin 8)   |

## Usage Examples

### Basic Usage

```python
from seeed_mr60bha2 import SEEED_MR60BHA2
import time

sensor = SEEED_MR60BHA2('/dev/serial0', debug=False)
sensor.begin()

try:
    while True:
        if sensor.update(timeout=0.1):
            # Get individual measurements
            heart_rate = sensor.get_heart_rate()
            breath_rate = sensor.get_breath_rate()
            distance = sensor.get_distance()
            phases = sensor.get_heart_breath_phases()

            if heart_rate:
                print(f"Heart Rate: {heart_rate:.2f} BPM")
            if breath_rate:
                print(f"Breath Rate: {breath_rate:.2f} BPM")
            if distance:
                print(f"Distance: {distance:.2f} m")
            if phases:
                print(f"Phases - Total: {phases.total_phase:.2f}, "
                      f"Breath: {phases.breath_phase:.2f}, "
                      f"Heart: {phases.heart_phase:.2f}")

        time.sleep(0.1)
finally:
    sensor.close()
```

### Using Context Manager

```python
from seeed_mr60bha2 import SEEED_MR60BHA2

# Automatic resource cleanup
with SEEED_MR60BHA2('/dev/serial0') as sensor:
    # Wait for specific measurements
    heart_rate = sensor.wait_for_heart_rate(timeout=5.0)
    if heart_rate:
        print(f"Heart Rate: {heart_rate:.2f} BPM")

    breath_rate = sensor.wait_for_breath_rate(timeout=5.0)
    if breath_rate:
        print(f"Breath Rate: {breath_rate:.2f} BPM")
```

### Getting All Data Without Consuming

```python
from seeed_mr60bha2 import SEEED_MR60BHA2

sensor = SEEED_MR60BHA2('/dev/serial0')
sensor.begin()

sensor.update()

# Get all data without marking it as consumed
data = sensor.get_all_data()

if data['heart_rate_valid']:
    print(f"Heart Rate: {data['heart_rate']:.2f} BPM")

if data['breath_rate_valid']:
    print(f"Breath Rate: {data['breath_rate']:.2f} BPM")

if data['distance_valid']:
    print(f"Distance: {data['distance']:.2f} m")

if data['phases_valid']:
    phases = data['phases']
    print(f"Total Phase: {phases.total_phase:.2f}")

sensor.close()
```

## API Reference

### SEEED_MR60BHA2 Class

#### Constructor

```python
SEEED_MR60BHA2(port, baud_rate=115200, timeout=1.0, debug=False)
```

- `port` (str): Serial port path (e.g., '/dev/serial0')
- `baud_rate` (int): Serial baud rate (default: 115200)
- `timeout` (float): Serial read timeout in seconds (default: 1.0)
- `debug` (bool): Enable debug logging (default: False)

#### Methods

##### `begin(reset_pin=None)`
Initialize the serial connection to the sensor.

##### `close()`
Close the serial connection.

##### `update(timeout=0.1)`
Fetch and process new frames from the sensor.
- Returns: `bool` - True if at least one frame was processed

##### `get_heart_rate()`
Get the latest heart rate measurement.
- Returns: `float` or `None` - Heart rate in BPM
- Note: Consumes the data (returns None on subsequent calls until new data arrives)

##### `get_breath_rate()`
Get the latest breath rate measurement.
- Returns: `float` or `None` - Breath rate in BPM
- Note: Consumes the data

##### `get_distance()`
Get the latest distance measurement.
- Returns: `float` or `None` - Distance in meters
- Note: Consumes the data

##### `get_heart_breath_phases()`
Get the latest phase information.
- Returns: `HeartBreathPhases` or `None`
- Note: Consumes the data

##### `get_all_data()`
Get all available sensor data without consuming it.
- Returns: `dict` with all current sensor data and validity flags

##### `wait_for_heart_rate(timeout=5.0)`
Wait for a heart rate measurement.
- `timeout` (float): Maximum time to wait in seconds
- Returns: `float` or `None` - Heart rate in BPM

##### `wait_for_breath_rate(timeout=5.0)`
Wait for a breath rate measurement.
- Returns: `float` or `None` - Breath rate in BPM

##### `wait_for_distance(timeout=5.0)`
Wait for a distance measurement.
- Returns: `float` or `None` - Distance in meters

### Data Classes

#### HeartBreathPhases

```python
@dataclass
class HeartBreathPhases:
    total_phase: float
    breath_phase: float
    heart_phase: float
```

## Examples

The library includes several example scripts in the `examples/` directory:

- **basic_usage.py**: Simple heart rate and breath rate monitoring
- **continuous_monitoring.py**: Continuous monitoring with CSV logging
- **context_manager_example.py**: Using context manager for automatic cleanup
- **real_time_display.py**: Real-time display with formatted output

Run examples:
```bash
cd examples
python3 basic_usage.py
```

## Troubleshooting

### Permission Denied Error

If you get a permission error when accessing `/dev/serial0`:

```bash
sudo usermod -a -G dialout $USER
# Log out and log back in for changes to take effect
```

### No Data Received

1. Check wiring connections
2. Verify UART is enabled: `ls -l /dev/serial0`
3. Make sure nothing else is using the serial port
4. Enable debug mode to see raw communication:
   ```python
   sensor = SEEED_MR60BHA2('/dev/serial0', debug=True)
   ```

### Sensor Not Detecting

- Ensure the sensor is powered (5V)
- Position yourself 0.5-1.5 meters in front of the sensor
- Stay still for a few seconds to allow the sensor to stabilize
- The sensor works best when pointed at the chest area

## Technical Details

### Communication Protocol

The sensor uses a binary protocol over UART at 115200 baud:

**Frame Structure:**
```
[SOF][ID_H][ID_L][LEN_H][LEN_L][TYPE_H][TYPE_L][HEAD_CKSUM][DATA...][DATA_CKSUM]
```

- **SOF**: Start of Frame (0x01)
- **ID**: Frame ID (big-endian uint16)
- **LEN**: Data length (big-endian uint16)
- **TYPE**: Frame type (big-endian uint16)
- **HEAD_CKSUM**: Header checksum (inverted XOR)
- **DATA**: Payload data
- **DATA_CKSUM**: Data checksum (inverted XOR)

### Frame Types

| Type   | Description              |
|--------|--------------------------|
| 0x0A13 | Heart/Breath Phase Data  |
| 0x0A14 | Breath Rate (BPM)        |
| 0x0A15 | Heart Rate (BPM)         |
| 0x0A16 | Distance (meters)        |

### Data Encoding

- Floats: IEEE 754 single-precision (little-endian)
- Integers: Little-endian format

## Development

### Project Structure

```
mmWave-python/
├── seeed_mr60bha2/
│   ├── __init__.py          # Package initialization
│   ├── exceptions.py        # Custom exceptions
│   ├── mmwave_base.py       # Base communication class
│   └── mr60bha2.py          # MR60BHA2 sensor implementation
├── examples/                 # Example scripts
│   ├── basic_usage.py
│   ├── continuous_monitoring.py
│   ├── context_manager_example.py
│   └── real_time_display.py
├── setup.py                 # Package installation
└── README.md                # This file
```

### Code Quality

The library follows Python best practices:
- PEP 8 style guide
- Type hints for better IDE support
- Comprehensive docstrings
- Proper error handling and logging
- Resource management with context managers

## License

This library is provided as-is for use with Seeed MR60BHA2 sensors.

## Credits

Based on the original C++ implementation for Arduino/ESP32.
Ported to Python by Andrea, 2025.

## Support

For issues, questions, or contributions, please open an issue on the repository.

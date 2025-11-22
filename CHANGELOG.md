# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-22

### Added
- Initial release of the Python library for Seeed MR60BHA2 mmWave sensor
- Complete port from C++/Arduino to pure Python
- Base communication class (`SeeedmmWave`) with frame handling
- MR60BHA2 sensor-specific implementation
- Support for heart rate monitoring (BPM)
- Support for breath rate monitoring (BPM)
- Support for distance measurement
- Support for phase data (total, breath, heart)
- Automatic frame parsing and checksum validation
- Comprehensive error handling and custom exceptions
- Logging support with configurable debug levels
- Context manager support for automatic resource cleanup
- Type hints throughout the codebase
- Full documentation with docstrings

### Examples
- Basic usage example
- Continuous monitoring with CSV logging
- Context manager usage example
- Real-time display with formatted output

### Documentation
- Comprehensive README with API reference
- Installation instructions for Raspberry Pi
- Wiring diagrams and troubleshooting guide
- Technical protocol documentation
- Multiple usage examples

### Development
- Package setup with setuptools
- Requirements file for dependencies
- Git ignore file
- MIT License

## Future Enhancements

Potential features for future releases:
- Support for sensor configuration commands
- Asynchronous I/O support with asyncio
- Data filtering and signal processing
- Graphical plotting capabilities
- MQTT integration for IoT applications
- REST API wrapper
- Unit tests and continuous integration

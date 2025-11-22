"""
Custom exceptions for the Seeed MR60BHA2 mmWave sensor library.

Author: AB-Engineering
Date: 2025-01-22
"""


class MmWaveError(Exception):
    """Base exception for all mmWave sensor errors."""
    pass


class MmWaveConnectionError(MmWaveError):
    """Exception raised when connection to the sensor fails."""
    pass


class MmWaveChecksumError(MmWaveError):
    """Exception raised when checksum validation fails."""
    pass


class MmWaveTimeoutError(MmWaveError):
    """Exception raised when a timeout occurs waiting for data."""
    pass


class MmWaveFrameError(MmWaveError):
    """Exception raised when frame parsing fails."""
    pass

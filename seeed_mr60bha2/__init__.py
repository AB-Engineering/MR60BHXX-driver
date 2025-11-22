"""
Seeed MR60BHA2 mmWave Sensor Library for Python.

This library provides a Python interface for the Seeed MR60BHA2 mmWave sensor,
which monitors heart rate and breathing rate using mmWave technology.

Example:
    >>> from seeed_mr60bha2 import SEEED_MR60BHA2
    >>> sensor = SEEED_MR60BHA2('/dev/serial0')
    >>> sensor.begin()
    >>> sensor.update()
    >>> heart_rate = sensor.get_heart_rate()

Author: AB-Engineering
Date: 2025-01-22
"""

from .mr60bha2 import SEEED_MR60BHA2, HeartBreathPhases, HeartBreathType
from .mmwave_base import SeeedmmWave
from .exceptions import (
    MmWaveError,
    MmWaveConnectionError,
    MmWaveChecksumError,
    MmWaveTimeoutError,
    MmWaveFrameError
)

__version__ = '1.0.0'
__author__ = 'AB-Engineering'

__all__ = [
    'SEEED_MR60BHA2',
    'HeartBreathPhases',
    'HeartBreathType',
    'SeeedmmWave',
    'MmWaveError',
    'MmWaveConnectionError',
    'MmWaveChecksumError',
    'MmWaveTimeoutError',
    'MmWaveFrameError',
]

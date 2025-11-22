"""
Seeed MR60BHA2 mmWave Heart Rate and Breath Monitoring Sensor.

This module provides the implementation for the MR60BHA2 sensor,
which monitors heart rate and breath rate using mmWave technology.

Author: AB-Engineering
Date: 2025-01-22
"""

import logging
from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, Tuple

from .mmwave_base import SeeedmmWave


class HeartBreathType(IntEnum):
    """Frame types for heart and breath data."""
    HEART_BREATH_PHASE = 0x0A13
    BREATH_RATE = 0x0A14
    HEART_RATE = 0x0A15
    HEART_BREATH_DISTANCE = 0x0A16


@dataclass
class HeartBreathPhases:
    """
    Heart and breath phase data.

    Attributes:
        total_phase: Total phase value
        breath_phase: Breathing phase value
        heart_phase: Heart phase value
    """
    total_phase: float
    breath_phase: float
    heart_phase: float


class SEEED_MR60BHA2(SeeedmmWave):
    """
    MR60BHA2 mmWave heart rate and breath monitoring sensor.

    This sensor monitors heart rate and breathing rate using mmWave technology.
    It provides real-time measurements of heart rate (BPM), breathing rate (BPM),
    phase information, and distance to the detected person.

    Example:
        >>> sensor = SEEED_MR60BHA2('/dev/serial0')
        >>> sensor.begin()
        >>> while True:
        ...     if sensor.update():
        ...         heart_rate = sensor.get_heart_rate()
        ...         breath_rate = sensor.get_breath_rate()
        ...         if heart_rate is not None:
        ...             print(f"Heart Rate: {heart_rate} BPM")
        ...         if breath_rate is not None:
        ...             print(f"Breath Rate: {breath_rate} BPM")
        ...     time.sleep(0.1)
    """

    def __init__(self, port: str, baud_rate: int = 115200,
                 timeout: float = 1.0, debug: bool = False):
        """
        Initialize the MR60BHA2 sensor.

        Args:
            port: Serial port path (e.g., '/dev/ttyUSB0' or '/dev/serial0')
            baud_rate: Serial communication baud rate (default: 115200)
            timeout: Serial read timeout in seconds
            debug: Enable debug logging
        """
        super().__init__(port, baud_rate, timeout, debug)

        # Heart and breath data
        self._heart_breath_phases: Optional[HeartBreathPhases] = None
        self._breath_rate: Optional[float] = None
        self._heart_rate: Optional[float] = None
        self._range_flag: Optional[int] = None
        self._range: Optional[float] = None

        # Data validity flags
        self._is_heart_breath_phase_valid = False
        self._is_breath_rate_valid = False
        self._is_heart_rate_valid = False
        self._is_distance_valid = False

    def handle_type(self, frame_type: int, data: bytes) -> bool:
        """
        Handle received frames based on their type.

        Args:
            frame_type: The frame type identifier
            data: The frame payload data

        Returns:
            True if handled successfully, False otherwise
        """
        try:
            frame_type_enum = HeartBreathType(frame_type)
        except ValueError:
            self._logger.debug(f"Unknown frame type: 0x{frame_type:04X}")
            return False

        if frame_type_enum == HeartBreathType.HEART_BREATH_PHASE:
            if len(data) < 12:  # 3 floats * 4 bytes
                self._logger.warning("Insufficient data for heart breath phase")
                return False

            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug(f"Raw phase data: {data[:12].hex(' ')}")

            total_phase = self._extract_float(data[0:4])
            breath_phase = self._extract_float(data[4:8])
            heart_phase = self._extract_float(data[8:12])

            self._heart_breath_phases = HeartBreathPhases(
                total_phase=total_phase,
                breath_phase=breath_phase,
                heart_phase=heart_phase
            )
            self._is_heart_breath_phase_valid = True
            self._logger.debug(f"Heart Breath Phase: total={total_phase:.2f}, "
                             f"breath={breath_phase:.2f}, heart={heart_phase:.2f}")
            return True

        elif frame_type_enum == HeartBreathType.BREATH_RATE:
            if len(data) < 4:  # 1 float * 4 bytes
                self._logger.warning("Insufficient data for breath rate")
                return False

            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug(f"Raw breath rate data: {data[:4].hex(' ')}")

            self._breath_rate = self._extract_float(data[0:4])
            self._is_breath_rate_valid = True
            self._logger.debug(f"Breath Rate: {self._breath_rate:.2f} BPM")
            return True

        elif frame_type_enum == HeartBreathType.HEART_RATE:
            if len(data) < 4:  # 1 float * 4 bytes
                self._logger.warning("Insufficient data for heart rate")
                return False

            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug(f"Raw heart rate data: {data[:4].hex(' ')}")

            self._heart_rate = self._extract_float(data[0:4])
            self._is_heart_rate_valid = True
            self._logger.debug(f"Heart Rate: {self._heart_rate:.2f} BPM")
            return True

        elif frame_type_enum == HeartBreathType.HEART_BREATH_DISTANCE:
            if len(data) < 8:  # 1 uint32 + 1 float
                self._logger.warning("Insufficient data for distance")
                return False

            # Debug: show raw bytes
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug(f"Raw distance data: {data[:8].hex(' ')}")

            self._range_flag = self._extract_uint32(data[0:4])
            self._range = self._extract_float(data[4:8])
            self._is_distance_valid = True
            self._logger.debug(f"Distance: flag={self._range_flag}, range={self._range:.2f}m")
            return True

        return False

    def get_heart_breath_phases(self) -> Optional[HeartBreathPhases]:
        """
        Get the latest heart and breath phase data.

        Returns:
            HeartBreathPhases object if data is valid, None otherwise

        Note:
            This method consumes the data (returns None on subsequent calls
            until new data arrives).
        """
        if not self._is_heart_breath_phase_valid:
            return None

        self._is_heart_breath_phase_valid = False
        return self._heart_breath_phases

    def get_breath_rate(self) -> Optional[float]:
        """
        Get the latest breath rate measurement.

        Returns:
            Breath rate in breaths per minute (BPM), or None if no valid data

        Note:
            This method consumes the data (returns None on subsequent calls
            until new data arrives).
        """
        if not self._is_breath_rate_valid:
            return None

        self._is_breath_rate_valid = False
        return self._breath_rate

    def get_heart_rate(self) -> Optional[float]:
        """
        Get the latest heart rate measurement.

        Returns:
            Heart rate in beats per minute (BPM), or None if no valid data

        Note:
            This method consumes the data (returns None on subsequent calls
            until new data arrives).
        """
        if not self._is_heart_rate_valid:
            return None

        self._is_heart_rate_valid = False
        return self._heart_rate

    def get_distance(self) -> Optional[float]:
        """
        Get the latest distance measurement.

        Returns:
            Distance in meters to the detected person, or None if no valid data

        Note:
            This method consumes the data (returns None on subsequent calls
            until new data arrives).
        """
        if not self._is_distance_valid or not self._range_flag:
            return None

        self._is_distance_valid = False
        return self._range

    def get_all_data(self) -> dict:
        """
        Get all available sensor data without consuming it.

        Returns:
            Dictionary with all current sensor data and validity flags

        Example:
            >>> data = sensor.get_all_data()
            >>> if data['heart_rate_valid']:
            ...     print(f"Heart Rate: {data['heart_rate']} BPM")
        """
        return {
            'heart_rate': self._heart_rate,
            'heart_rate_valid': self._is_heart_rate_valid,
            'breath_rate': self._breath_rate,
            'breath_rate_valid': self._is_breath_rate_valid,
            'phases': self._heart_breath_phases,
            'phases_valid': self._is_heart_breath_phase_valid,
            'distance': self._range,
            'distance_valid': self._is_distance_valid and bool(self._range_flag),
        }

    def wait_for_heart_rate(self, timeout: float = 5.0) -> Optional[float]:
        """
        Wait for a heart rate measurement.

        Args:
            timeout: Maximum time to wait in seconds

        Returns:
            Heart rate in BPM, or None if timeout occurs
        """
        if self.fetch_type(HeartBreathType.HEART_RATE, timeout):
            return self.get_heart_rate()
        return None

    def wait_for_breath_rate(self, timeout: float = 5.0) -> Optional[float]:
        """
        Wait for a breath rate measurement.

        Args:
            timeout: Maximum time to wait in seconds

        Returns:
            Breath rate in BPM, or None if timeout occurs
        """
        if self.fetch_type(HeartBreathType.BREATH_RATE, timeout):
            return self.get_breath_rate()
        return None

    def wait_for_distance(self, timeout: float = 5.0) -> Optional[float]:
        """
        Wait for a distance measurement.

        Args:
            timeout: Maximum time to wait in seconds

        Returns:
            Distance in meters, or None if timeout occurs
        """
        if self.fetch_type(HeartBreathType.HEART_BREATH_DISTANCE, timeout):
            return self.get_distance()
        return None

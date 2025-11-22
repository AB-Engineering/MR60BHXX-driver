"""
Base class for Seeed mmWave sensor communication.

This module provides the core communication protocol implementation for
mmWave sensors, including frame construction, parsing, and checksum validation.

Author: AB-Engineering
Date: 2025-01-22
"""

import struct
import sys
import time
import logging
from abc import ABC, abstractmethod
from collections import deque
from typing import Optional, List, Tuple

import serial

from .exceptions import (
    MmWaveConnectionError,
    MmWaveChecksumError,
    MmWaveFrameError,
    MmWaveTimeoutError
)


# Frame structure constants
SOF_BYTE = 0x01
SIZE_SOF = 1
SIZE_ID = 2
SIZE_LEN = 2
SIZE_TYPE = 2
SIZE_HEAD_CKSUM = 1
SIZE_FRAME_HEADER = SIZE_SOF + SIZE_ID + SIZE_LEN + SIZE_TYPE + SIZE_HEAD_CKSUM
SIZE_DATA_CKSUM = 1

# Configuration constants
DEFAULT_BAUD_RATE = 115200
FRAME_BUFFER_SIZE = 512
MAX_QUEUE_SIZE = 120
MAX_FRAME_DATA_SIZE = 30


class SeeedmmWave(ABC):
    """
    Base class for Seeed mmWave sensor communication.

    This class handles the low-level serial communication, frame construction,
    parsing, and checksum validation for mmWave sensors.

    Attributes:
        port (str): Serial port path (e.g., '/dev/ttyUSB0' or '/dev/serial0')
        baud_rate (int): Serial communication baud rate (default: 115200)
        timeout (float): Serial read timeout in seconds
    """

    def __init__(self, port: str, baud_rate: int = DEFAULT_BAUD_RATE,
                 timeout: float = 1.0, debug: bool = False):
        """
        Initialize the mmWave sensor communication.

        Args:
            port: Serial port path (e.g., '/dev/ttyUSB0' or '/dev/serial0')
            baud_rate: Serial communication baud rate (default: 115200)
            timeout: Serial read timeout in seconds
            debug: Enable debug logging
        """
        self._port = port
        self._baud_rate = baud_rate
        self._timeout = timeout
        self._serial: Optional[serial.Serial] = None
        self._frame_id = 0x8000
        self._frame_queue: deque = deque(maxlen=MAX_QUEUE_SIZE)

        # Setup logging
        self._logger = logging.getLogger(self.__class__.__name__)
        if debug:
            self._logger.setLevel(logging.DEBUG)
            if not self._logger.handlers:
                handler = logging.StreamHandler()
                handler.setFormatter(logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                ))
                self._logger.addHandler(handler)
        else:
            self._logger.setLevel(logging.WARNING)

    def begin(self, reset_pin: Optional[int] = None) -> None:
        """
        Initialize the serial connection to the sensor.

        Args:
            reset_pin: GPIO pin number for hardware reset (not implemented for Raspberry Pi)

        Raises:
            MmWaveConnectionError: If connection fails
        """
        try:
            self._serial = serial.Serial(
                port=self._port,
                baudrate=self._baud_rate,
                timeout=self._timeout,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )

            # Clear any existing data in buffers
            self._serial.reset_input_buffer()
            self._serial.reset_output_buffer()

            self._logger.info(f"Connected to sensor on {self._port} at {self._baud_rate} baud")

            # Hardware reset not implemented for Raspberry Pi
            # Could be implemented using RPi.GPIO if needed
            if reset_pin is not None:
                self._logger.warning("Hardware reset via GPIO not implemented")

        except serial.SerialException as e:
            raise MmWaveConnectionError(f"Failed to connect to {self._port}: {e}")

    def close(self) -> None:
        """Close the serial connection."""
        if self._serial and self._serial.is_open:
            self._serial.close()
            self._logger.info("Serial connection closed")

    def __enter__(self):
        """Context manager entry."""
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def _calculate_checksum(self, data: bytes) -> int:
        """
        Calculate XOR checksum for data.

        Args:
            data: Bytes to calculate checksum for

        Returns:
            Calculated checksum (inverted XOR)
        """
        checksum = 0
        for byte in data:
            checksum ^= byte
        return (~checksum) & 0xFF

    def _validate_checksum(self, data: bytes, expected_checksum: int) -> bool:
        """
        Validate checksum of data.

        Args:
            data: Data bytes to validate
            expected_checksum: Expected checksum value

        Returns:
            True if checksum is valid, False otherwise
        """
        return self._calculate_checksum(data) == expected_checksum

    def _extract_float(self, data: bytes) -> float:
        """
        Extract a float value from bytes (little-endian).

        Args:
            data: 4 bytes representing a float

        Returns:
            Extracted float value
        """
        return struct.unpack('<f', data[:4])[0]

    def _extract_uint32(self, data: bytes) -> int:
        """
        Extract a uint32 value from bytes (little-endian).

        Args:
            data: 4 bytes representing a uint32

        Returns:
            Extracted uint32 value
        """
        return struct.unpack('<I', data[:4])[0]

    def _float_to_bytes(self, value: float) -> bytes:
        """
        Convert a float to bytes (little-endian).

        Args:
            value: Float value to convert

        Returns:
            4 bytes representing the float
        """
        return struct.pack('<f', value)

    def _uint32_to_bytes(self, value: int) -> bytes:
        """
        Convert a uint32 to bytes (little-endian).

        Args:
            value: Uint32 value to convert

        Returns:
            4 bytes representing the uint32
        """
        return struct.pack('<I', value)

    def _packet_frame(self, frame_type: int, data: Optional[bytes] = None) -> bytes:
        """
        Construct a complete frame with header and checksums.

        Frame structure:
        [SOF][ID_H][ID_L][LEN_H][LEN_L][TYPE_H][TYPE_L][HEAD_CKSUM][DATA...][DATA_CKSUM]

        Args:
            frame_type: Frame type identifier (16-bit)
            data: Optional payload data

        Returns:
            Complete frame as bytes
        """
        data_len = len(data) if data else 0

        # Construct header using struct for proper byte packing
        frame = bytearray()
        frame.append(SOF_BYTE)  # Start of Frame
        frame.extend(struct.pack('>H', self._frame_id))  # ID (big-endian uint16)
        frame.extend(struct.pack('>H', data_len))  # Length (big-endian uint16)
        frame.extend(struct.pack('>H', frame_type))  # Type (big-endian uint16)

        # Calculate and append header checksum
        head_checksum = self._calculate_checksum(bytes(frame))
        frame.append(head_checksum)

        # Add data and data checksum if present
        if data:
            frame.extend(data)
            data_checksum = self._calculate_checksum(data)
            frame.append(data_checksum)

        # Increment frame ID (Pythonic way)
        self._frame_id = ((self._frame_id + 1) & 0xFFFF) or 0x8000

        return bytes(frame)

    def _send_frame(self, frame: bytes) -> bool:
        """
        Send a frame over the serial connection.

        Args:
            frame: Complete frame to send

        Returns:
            True if successful, False otherwise
        """
        if not self._serial or not self._serial.is_open:
            self._logger.error("Serial port not open")
            return False

        try:
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug(f"Send >>> {frame.hex(' ')}")

            bytes_sent = self._serial.write(frame)
            self._serial.flush()

            return bytes_sent == len(frame)
        except serial.SerialException as e:
            self._logger.error(f"Failed to send frame: {e}")
            return False

    def send(self, frame_type: int, data: Optional[bytes] = None) -> bool:
        """
        Construct and send a frame.

        Args:
            frame_type: Frame type identifier
            data: Optional payload data

        Returns:
            True if successful, False otherwise
        """
        frame = self._packet_frame(frame_type, data)
        return self._send_frame(frame)

    def _process_frame(self, frame: bytes, expected_type: Optional[int] = None) -> bool:
        """
        Process a received frame.

        Args:
            frame: Complete frame bytes
            expected_type: Expected frame type (None = accept any)

        Returns:
            True if frame processed successfully, False otherwise
        """
        if len(frame) < SIZE_FRAME_HEADER:
            self._logger.warning("Frame too short")
            return False

        # Parse header using struct for better Python compliance
        sof = frame[0]
        frame_id = struct.unpack('>H', frame[1:3])[0]  # Big-endian uint16
        data_len = struct.unpack('>H', frame[3:5])[0]  # Big-endian uint16
        frame_type = struct.unpack('>H', frame[5:7])[0]  # Big-endian uint16
        head_checksum = frame[7]

        # Validate SOF
        if sof != SOF_BYTE:
            self._logger.warning(f"Invalid SOF: 0x{sof:02X}")
            return False

        # Validate expected frame length
        expected_len = SIZE_FRAME_HEADER + data_len + SIZE_DATA_CKSUM
        if len(frame) != expected_len:
            self._logger.warning(f"Frame length mismatch: got {len(frame)}, expected {expected_len}")
            return False

        # Validate header checksum
        if not self._validate_checksum(frame[:SIZE_FRAME_HEADER - SIZE_HEAD_CKSUM], head_checksum):
            self._logger.warning("Header checksum validation failed")
            raise MmWaveChecksumError("Header checksum validation failed")

        # Extract data and validate data checksum
        if data_len > 0:
            data = frame[SIZE_FRAME_HEADER:SIZE_FRAME_HEADER + data_len]
            data_checksum = frame[SIZE_FRAME_HEADER + data_len]

            if not self._validate_checksum(data, data_checksum):
                self._logger.warning("Data checksum validation failed")
                raise MmWaveChecksumError("Data checksum validation failed")
        else:
            data = b''

        # Check if type matches expected type
        if expected_type is not None and frame_type != expected_type:
            return False

        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(f"Recv <<< Type: 0x{frame_type:04X}, Data: {data.hex(' ')}")

        # Handle the frame type
        return self.handle_type(frame_type, data)

    @abstractmethod
    def handle_type(self, frame_type: int, data: bytes) -> bool:
        """
        Handle a received frame based on its type.

        This method must be implemented by derived classes to process
        specific frame types.

        Args:
            frame_type: The frame type identifier
            data: The frame payload data

        Returns:
            True if handled successfully, False otherwise
        """
        pass

    def fetch(self, timeout: float = 1.0) -> None:
        """
        Read and queue frames from the serial port.

        Args:
            timeout: Maximum time to spend reading (seconds)
        """
        if not self._serial or not self._serial.is_open:
            return

        start_time = time.time()
        frame_buffer = bytearray()
        in_frame = False

        while time.time() - start_time < timeout:
            # Check for available data
            if self._serial.in_waiting == 0:
                time.sleep(0.001)  # Small delay to prevent busy waiting
                continue

            byte = self._serial.read(1)
            if not byte:
                continue

            byte_val = byte[0]

            if in_frame:
                frame_buffer.append(byte_val)

                # Check if we have enough for header
                if len(frame_buffer) >= SIZE_FRAME_HEADER:
                    # Extract data length from header
                    data_len = struct.unpack('>H', frame_buffer[3:5])[0]

                    # Sanity check on data length
                    if data_len > MAX_FRAME_DATA_SIZE:
                        self._logger.warning(f"Data length too large: {data_len}, resynchronizing")
                        # This is likely a false SOF detection, resynchronize
                        in_frame = False
                        frame_buffer.clear()
                        continue

                    # Check if we have complete frame
                    expected_len = SIZE_FRAME_HEADER + data_len + SIZE_DATA_CKSUM
                    if len(frame_buffer) == expected_len:
                        # Validate header checksum before accepting frame
                        head_checksum = frame_buffer[7]
                        if self._validate_checksum(bytes(frame_buffer[:7]), head_checksum):
                            # Frame complete and valid, add to queue
                            if self._logger.isEnabledFor(logging.DEBUG):
                                self._logger.debug(f"Frame queued: {bytes(frame_buffer).hex(' ')}")

                            self._frame_queue.append(bytes(frame_buffer))
                        else:
                            # Invalid checksum, probably false SOF
                            self._logger.warning("Invalid header checksum, resynchronizing")

                        in_frame = False
                        frame_buffer.clear()
            else:
                # Looking for start of frame
                if byte_val == SOF_BYTE:
                    in_frame = True
                    frame_buffer.clear()
                    frame_buffer.append(byte_val)

    def process_queued_frames(self, expected_type: Optional[int] = None,
                            timeout: float = 1.0) -> bool:
        """
        Process all queued frames.

        Args:
            expected_type: Only process frames of this type (None = all types)
            timeout: Maximum time to spend processing (seconds)

        Returns:
            True if at least one frame was processed successfully
        """
        if not self._frame_queue:
            return False

        result = False
        start_time = time.time()

        while self._frame_queue and (time.time() - start_time < timeout):
            frame = self._frame_queue.popleft()

            try:
                if self._process_frame(frame, expected_type):
                    result = True
            except MmWaveChecksumError as e:
                self._logger.warning(f"Checksum error: {e}")
                continue

        return result

    def update(self, timeout: float = 0.1) -> bool:
        """
        Fetch and process new frames.

        Args:
            timeout: Maximum time to wait for frames (seconds)

        Returns:
            True if at least one frame was processed successfully
        """
        self.fetch(timeout)
        return self.process_queued_frames(timeout=timeout)

    def fetch_type(self, frame_type: int, timeout: float = 1.0) -> bool:
        """
        Fetch frames and process only specific type.

        Args:
            frame_type: Frame type to wait for
            timeout: Maximum time to wait (seconds)

        Returns:
            True if frame of requested type was received and processed
        """
        self.fetch(timeout)
        return self.process_queued_frames(expected_type=frame_type, timeout=timeout)

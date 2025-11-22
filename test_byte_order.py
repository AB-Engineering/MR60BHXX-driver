#!/usr/bin/env python3
"""
Test to verify correct byte order for float and uint32 parsing.

This will help diagnose if the issue is endianness-related.
"""

import struct


def test_conversions():
    """Test various byte order scenarios."""

    print("="*70)
    print(" Byte Order Test")
    print("="*70)

    # Test 1: Distance value you're seeing (74.62m)
    print("\n1. Testing the 74.62m value you're seeing:")
    distance_value = 74.62

    # How would this be encoded in different formats?
    little_endian = struct.pack('<f', distance_value)
    big_endian = struct.pack('>f', distance_value)

    print(f"   74.62 as little-endian: {little_endian.hex(' ')}")
    print(f"   74.62 as big-endian:    {big_endian.hex(' ')}")

    # What if we swap?
    print(f"   If we read little as big: {struct.unpack('>f', little_endian)[0]:.2f}")
    print(f"   If we read big as little: {struct.unpack('<f', big_endian)[0]:.2f}")

    # Test 2: Expected distance (0.25m = 25cm)
    print("\n2. Testing expected distance (0.25m = 25cm):")
    expected_distance = 0.25

    little_endian = struct.pack('<f', expected_distance)
    big_endian = struct.pack('>f', expected_distance)

    print(f"   0.25 as little-endian: {little_endian.hex(' ')}")
    print(f"   0.25 as big-endian:    {big_endian.hex(' ')}")

    # What if we swap?
    print(f"   If we read little as big: {struct.unpack('>f', little_endian)[0]:.10f}")
    print(f"   If we read big as little: {struct.unpack('<f', big_endian)[0]:.10f}")

    # Test 3: Check if 0.25m little-endian read as big-endian gives us 74.62
    test_bytes = struct.pack('<f', 0.25)
    result = struct.unpack('>f', test_bytes)[0]
    print(f"\n3. Does 0.25m (little) read as big give 74.62? {result:.2f}")

    # Test 4: Common heart/breath rates
    print("\n4. Testing heart rate (71 BPM):")
    hr = 71.0
    little_endian = struct.pack('<f', hr)
    big_endian = struct.pack('>f', hr)

    print(f"   71.0 as little-endian: {little_endian.hex(' ')}")
    print(f"   71.0 as big-endian:    {big_endian.hex(' ')}")

    print("\n5. Testing breath rate (20 BPM):")
    br = 20.0
    little_endian = struct.pack('<f', br)
    big_endian = struct.pack('>f', br)

    print(f"   20.0 as little-endian: {little_endian.hex(' ')}")
    print(f"   20.0 as big-endian:    {big_endian.hex(' ')}")

    # Test 6: The problematic data length (55433)
    print("\n6. Testing the data length value (55433 = 0xD889):")
    print(f"   As big-endian uint16: 0xD8 0x89")
    print(f"   As little-endian uint16: 0x89 0xD8")
    print(f"   If these bytes are actually little-endian, value would be:")
    print(f"   {struct.unpack('<H', bytes([0xD8, 0x89]))[0]}")

    # Check if this could be a valid ID or TYPE field
    print(f"\n   Could this be part of a valid frame?")
    print(f"   Type field values we expect: 0x0A13, 0x0A14, 0x0A15, 0x0A16")
    print(f"   0xD889 doesn't match any expected type")

    print("\n" + "="*70)
    print("CONCLUSION:")
    print("The 74.62m reading when you're at 25cm suggests a possible")
    print("endianness mismatch or frame synchronization issue.")
    print("="*70)


if __name__ == '__main__':
    test_conversions()

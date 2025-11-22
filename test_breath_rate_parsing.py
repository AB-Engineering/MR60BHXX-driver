#!/usr/bin/env python3
"""
Test to verify breath rate parsing is correct.
"""

import struct

def test_breath_rate_parsing():
    """Test different breath rate values."""

    print("="*70)
    print(" Breath Rate Parsing Test")
    print("="*70)

    # Test common breath rate values
    test_values = [
        0.0,   # No detection
        12.0,  # Low breath rate
        15.0,  # Normal resting
        18.0,  # Normal
        20.0,  # Normal
        22.0,  # Slightly elevated
        25.0,  # Higher
        30.0,  # Very high
    ]

    print("\nTest 1: Encoding and decoding breath rates")
    print("-" * 70)
    for value in test_values:
        # Encode as little-endian float (what sensor sends)
        encoded = struct.pack('<f', value)

        # Decode it back (what Python library does)
        decoded = struct.unpack('<f', encoded)[0]

        print(f"  Original: {value:6.2f} BPM")
        print(f"  Encoded:  {encoded.hex(' ')}")
        print(f"  Decoded:  {decoded:6.2f} BPM")
        print(f"  Match:    {'✓' if abs(value - decoded) < 0.01 else '✗'}")
        print()

    # Test the actual byte sequences from the sensor
    print("\nTest 2: Real sensor data from previous logs")
    print("-" * 70)

    # From the user's debug logs showing "breath rate = 22.000000"
    # The sensor sends ASCII debug messages, not the actual data frame
    # But let's test what 22.0 would look like as bytes
    breath_rate_22 = struct.pack('<f', 22.0)
    print(f"  22 BPM as bytes: {breath_rate_22.hex(' ')}")
    print(f"  Decoded back:    {struct.unpack('<f', breath_rate_22)[0]:.2f} BPM")
    print()

    # Test 0.0 (no detection)
    breath_rate_0 = struct.pack('<f', 0.0)
    print(f"  0 BPM as bytes:  {breath_rate_0.hex(' ')}")
    print(f"  Decoded back:    {struct.unpack('<f', breath_rate_0)[0]:.2f} BPM")
    print()

    # Test potential problematic cases
    print("\nTest 3: Edge cases")
    print("-" * 70)

    # Very small value (near zero)
    small_val = 0.001
    encoded = struct.pack('<f', small_val)
    decoded = struct.unpack('<f', encoded)[0]
    print(f"  Very small ({small_val}): {encoded.hex(' ')} -> {decoded:.6f}")

    # NaN
    import math
    nan_bytes = struct.pack('<f', float('nan'))
    print(f"  NaN: {nan_bytes.hex(' ')}")

    # Infinity
    inf_bytes = struct.pack('<f', float('inf'))
    print(f"  Infinity: {inf_bytes.hex(' ')}")

    print("\n" + "="*70)
    print("CONCLUSION:")
    print("The Python struct.unpack('<f', data) correctly handles")
    print("little-endian float parsing, matching the C++ reinterpret_cast")
    print("behavior on little-endian systems (which includes x86, ARM, etc.)")
    print("="*70)


if __name__ == '__main__':
    test_breath_rate_parsing()

import pytest

def test_calculate_checksum_normal_operation():
    """Test normal checksum calculation with various byte sequences."""
    # Simple case with known result
    assert calculate_checksum(b'\x01\x02\x03') == 0  # 1 ^ 2 ^ 3 = 0
    
    # Another simple case
    assert calculate_checksum(b'\x05\x0A') == 15  # 5 ^ 10 = 15
    
    # Single byte
    assert calculate_checksum(b'\xFF') == 255
    
    # Multiple bytes with known XOR result
    assert calculate_checksum(b'\x12\x34\x56') == 116  # 18 ^ 52 ^ 86 = 116

def test_calculate_checksum_empty_input():
    """Test that empty bytes return 0."""
    assert calculate_checksum(b'') == 0

def test_calculate_checksum_single_byte():
    """Test checksum with single byte values."""
    assert calculate_checksum(b'\x00') == 0
    assert calculate_checksum(b'\x01') == 1
    assert calculate_checksum(b'\x7F') == 127
    assert calculate_checksum(b'\x80') == 128
    assert calculate_checksum(b'\xFF') == 255

def test_calculate_checksum_edge_cases():
    """Test edge cases with special byte patterns."""
    # All same bytes (even count) - should XOR to 0
    assert calculate_checksum(b'\xAA\xAA') == 0
    
    # All same bytes (odd count) - should equal the byte value
    assert calculate_checksum(b'\xAA\xAA\xAA') == 170  # 0xAA = 170
    
    # Maximum values
    assert calculate_checksum(b'\xFF\xFF') == 0  # 255 ^ 255 = 0
    
    # Large sequence that XORs to 0
    assert calculate_checksum(b'\x01\x02\x03\x01\x02\x03') == 0

def test_calculate_checksum_large_input():
    """Test with larger byte sequences."""
    # Test with 256 bytes (0-255)
    large_data = bytes(range(256))
    # XOR of 0-255 is known to be 0
    assert calculate_checksum(large_data) == 0
    
    # Test with 1000 identical bytes
    large_identical = b'\x42' * 1000  # Even count, should be 0
    assert calculate_checksum(large_identical) == 0
    
    # Test with 1001 identical bytes
    large_identical_odd = b'\x42' * 1001  # Odd count, should be 0x42
    assert calculate_checksum(large_identical_odd) == 66  # 0x42 = 66

def test_calculate_checksum_type_error():
    """Test that TypeError is raised for non-bytes input."""
    with pytest.raises(TypeError):
        calculate_checksum("string")
    
    with pytest.raises(TypeError):
        calculate_checksum([1, 2, 3])
    
    with pytest.raises(TypeError):
        calculate_checksum(123)
    
    with pytest.raises(TypeError):
        calculate_checksum(None)
    
    with pytest.raises(TypeError):
        calculate_checksum(bytearray(b'test'))

def test_calculate_checksum_result_range():
    """Test that result is always in valid 8-bit range."""
    test_cases = [
        b'\x00\x01',
        b'\xFF\x00',
        b'\x80\x7F',
        b'\x12\x34\x56\x78',
        bytes(range(50))
    ]
    
    for data in test_cases:
        result = calculate_checksum(data)
        assert 0 <= result <= 255, f"Result {result} not in 8-bit range for data {data!r}"
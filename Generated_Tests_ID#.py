```python
import pytest


def calculate_checksum(data: bytes) -> int:
    """
    Calculates an 8-bit checksum by XORing all bytes together.
    Returns 0 for empty input.
    Raises TypeError if input is not bytes.
    """
    if not isinstance(data, bytes):
        raise TypeError("Input must be bytes")
    
    if len(data) == 0:
        return 0
    
    checksum = 0
    for byte in data:
        checksum ^= byte
    
    return checksum


class TestCalculateChecksum:
    """Test cases for calculate_checksum function"""
    
    # Normal operation tests
    def test_single_byte(self):
        """Test checksum with a single byte"""
        assert calculate_checksum(b'\x42') == 0x42
    
    def test_two_bytes(self):
        """Test checksum with two bytes"""
        assert calculate_checksum(b'\x42\x24') == (0x42 ^ 0x24)
    
    def test_multiple_bytes(self):
        """Test checksum with multiple bytes"""
        assert calculate_checksum(b'\x01\x02\x03\x04') == (0x01 ^ 0x02 ^ 0x03 ^ 0x04)
    
    def test_ascii_string(self):
        """Test checksum with ASCII text"""
        data = b'hello'
        expected = ord('h') ^ ord('e') ^ ord('l') ^ ord('l') ^ ord('o')
        assert calculate_checksum(data) == expected
    
    def test_known_result(self):
        """Test with known checksum result"""
        # XOR of [0xAA, 0x55] = 0xFF
        assert calculate_checksum(b'\xAA\x55') == 0xFF
    
    def test_identical_bytes_even_count(self):
        """Test XOR property: even number of identical bytes = 0"""
        assert calculate_checksum(b'\x42\x42') == 0
        assert calculate_checksum(b'\xFF\xFF\xFF\xFF') == 0
    
    def test_identical_bytes_odd_count(self):
        """Test XOR property: odd number of identical bytes = byte value"""
        assert calculate_checksum(b'\x42\x42\x42') == 0x42
    
    # Edge cases
    def test_empty_bytes(self):
        """Test with empty bytes input"""
        assert calculate_checksum(b'') == 0
    
    def test_zero_byte(self):
        """Test with zero byte"""
        assert calculate_checksum(b'\x00') == 0
    
    def test_max_byte_value(self):
        """Test with maximum byte value (0xFF)"""
        assert calculate_checksum(b'\xFF') == 0xFF
    
    def test_all_zeros(self):
        """Test with multiple zero bytes"""
        assert calculate_checksum(b'\x00\x00\x00\x00') == 0
    
    def test_all_ones(self):
        """Test with all 0xFF bytes (odd count)"""
        assert calculate_checksum(b'\xFF\xFF\xFF') == 0xFF
    
    def test_large_data(self):
        """Test with large amount of data"""
        data = bytes(range(256))
        result = calculate_checksum(data)
        assert isinstance(result, int)
        assert 0 <= result <= 255
    
    def test_binary_data(self):
        """Test with arbitrary binary data"""
        data = bytes([0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77])
        expected = 0x00 ^ 0x11 ^ 0x22 ^ 0x33 ^ 0x44 ^ 0x55 ^ 0x66 ^ 0x77
        assert calculate_checksum(data) == expected
    
    def test_result_is_8bit(self):
        """Test that result is always within 8-bit range"""
        test_cases = [
            b'\xFF\xFF',
            b'\x00\xFF\x00\xFF',
            bytes(range(100)),
        ]
        for data in test_cases:
            result = calculate_checksum(data)
            assert 0 <= result <= 255
    
    # Error conditions
    def test_none_input(self):
        """Test that None raises TypeError"""
        with pytest.raises(TypeError):
            calculate_checksum(None)
    
    def test_string_input(self):
        """Test that string raises TypeError"""
        with pytest.raises(TypeError):
            calculate_checksum("hello")
    
    def test_int_input(self):
        """Test that integer raises TypeError"""
        with pytest.raises(TypeError):
            calculate_checksum(12345)
    
    def test_list_input(self):
        """Test that list raises TypeError"""
        with pytest.raises(TypeError):
            calculate_checksum([1, 2, 3, 4])
    
    def test_bytearray_input(self):
        """Test that bytearray raises TypeError (not bytes)"""
        with pytest.raises(TypeError):
            calculate_checksum(bytearray(b'hello'))
    
    def test_float_input(self):
        """Test that float raises TypeError"""
        with pytest.raises(TypeError):
            calculate_checksum(3.14)
    
    def test_dict_input(self):
        """Test that dict raises TypeError"""
        with pytest.raises(TypeError):
            calculate_checksum({})
```
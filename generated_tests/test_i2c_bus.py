import pytest
from i2c_controller import I2CController, I2CError

# Test fixtures
@pytest.fixture
def i2c():
    """Initialize I2C controller for testing"""
    controller = I2CController()
    reset_controller()
    return controller

@pytest.fixture
def valid_device_addr():
    """Valid 7-bit I2C device address"""
    return 0x48

@pytest.fixture
def invalid_device_addr():
    """Invalid I2C device address (no device present)"""
    return 0x7F

class TestI2CBasicOperations:
    """Test basic I2C operations with valid parameters"""
    
    def test_write_single_byte(self, i2c, valid_device_addr):
        """Test writing a single byte"""
        data = b'\x42'
        result = i2c_write(valid_device_addr, data)
        assert result is None  # Success returns None
    
    def test_write_multiple_bytes(self, i2c, valid_device_addr):
        """Test writing multiple bytes"""
        data = b'\x01\x02\x03\x04'
        result = i2c_write(valid_device_addr, data)
        assert result is None
    
    def test_read_single_byte(self, i2c, valid_device_addr):
        """Test reading a single byte"""
        data = i2c_read(valid_device_addr, 1)
        assert isinstance(data, bytes)
        assert len(data) == 1
    
    def test_read_multiple_bytes(self, i2c, valid_device_addr):
        """Test reading multiple bytes"""
        length = 4
        data = i2c_read(valid_device_addr, length)
        assert isinstance(data, bytes)
        assert len(data) == length
    
    def test_write_then_read(self, i2c, valid_device_addr):
        """Test write then read operation (register access)"""
        write_data = b'\x10'  # Register address
        read_length = 2
        data = i2c_write_read(valid_device_addr, write_data, read_length)
        assert isinstance(data, bytes)
        assert len(data) == read_length
    
    def test_probe_existing_device(self, i2c, valid_device_addr):
        """Test probing an existing device"""
        result = i2c_probe(valid_device_addr)
        assert result is True
    
    def test_probe_non_existing_device(self, i2c, invalid_device_addr):
        """Test probing a non-existing device"""
        result = i2c_probe(invalid_device_addr)
        assert result is False

class TestI2CBoundaryConditions:
    """Test boundary conditions for transfer sizes"""
    
    def test_write_max_size(self, i2c, valid_device_addr):
        """Test writing maximum allowed bytes (256)"""
        data = b'\x55' * 256
        result = i2c_write(valid_device_addr, data)
        assert result is None
    
    def test_read_max_size(self, i2c, valid_device_addr):
        """Test reading maximum allowed bytes (256)"""
        data = i2c_read(valid_device_addr, 256)
        assert isinstance(data, bytes)
        assert len(data) == 256
    
    def test_read_min_size(self, i2c, valid_device_addr):
        """Test reading minimum allowed bytes (1)"""
        data = i2c_read(valid_device_addr, 1)
        assert isinstance(data, bytes)
        assert len(data) == 1
    
    def test_write_empty_data(self, i2c, valid_device_addr):
        """Test writing empty data"""
        data = b''
        result = i2c_write(valid_device_addr, data)
        assert result is None

class TestI2CErrorHandling:
    """Test error handling scenarios"""
    
    def test_write_nack_error(self, i2c, invalid_device_addr):
        """Test NACK error on write operation"""
        data = b'\x42'
        with pytest.raises(I2CError, match="NACK"):
            i2c_write(invalid_device_addr, data)
    
    def test_read_nack_error(self, i2c, invalid_device_addr):
        """Test NACK error on read operation"""
        with pytest.raises(I2CError, match="NACK"):
            i2c_read(invalid_device_addr, 1)
    
    def test_write_then_read_nack_error(self, i2c, invalid_device_addr):
        """Test NACK error on write then read operation"""
        write_data = b'\x10'
        with pytest.raises(I2CError, match="NACK"):
            i2c_write_read(invalid_device_addr, write_data, 1)
    
    def test_timeout_error(self, i2c, valid_device_addr):
        """Test timeout error handling"""
        # Simulate timeout condition
        with pytest.raises(I2CError, match="TIMEOUT"):
            # This would be triggered by hardware simulation
            i2c_write(valid_device_addr, b'\x42')
    
    def test_bus_busy_error(self, i2c, valid_device_addr):
        """Test bus busy error handling"""
        with pytest.raises(I2CError, match="BUS_BUSY"):
            # This would be triggered by hardware simulation
            i2c_write(valid_device_addr, b'\x42')

class TestI2CParameterValidation:
    """Test parameter validation"""
    
    def test_invalid_device_address_range(self, i2c):
        """Test invalid device address (> 0x7F for 7-bit mode)"""
        with pytest.raises(ValueError, match="Invalid device address"):
            i2c_write(0x80, b'\x42')  # Invalid for 7-bit addressing
    
    def test_read_length_zero(self, i2c, valid_device_addr):
        """Test read with zero length"""
        with pytest.raises(ValueError, match="Invalid length"):
            i2c_read(valid_device_addr, 0)
    
    def test_read_length_too_large(self, i2c, valid_device_addr):
        """Test read with length > 256"""
        with pytest.raises(ValueError, match="Invalid length"):
            i2c_read(valid_device_addr, 257)
    
    def test_write_data_too_large(self, i2c, valid_device_addr):
        """Test write with data > 256 bytes"""
        data = b'\x55' * 257
        with pytest.raises(ValueError, match="Data too large"):
            i2c_write(valid_device_addr, data)

class TestI2CConfiguration:
    """Test I2C controller configuration"""
    
    def test_clock_speed_configuration(self, i2c):
        """Test that clock speed is configured correctly"""
        assert i2c.config.clock_speed_hz == 400000
    
    def test_address_mode_configuration(self, i2c):
        """Test that address mode is configured correctly"""
        assert i2c.config.address_mode == "7-bit"
    
    def test_timeout_configuration(self, i2c):
        """Test that timeout is configured correctly"""
        assert i2c.config.timeout_ms == 100
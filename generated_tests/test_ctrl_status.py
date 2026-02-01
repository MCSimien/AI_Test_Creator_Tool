# Register and field constants
CTRL_STATUS_ADDR = 4096
CTRL_STATUS_RESET_VALUE = 0

# Field bit masks
ENABLE_MASK = 0x1
READY_MASK = 0x2
MODE_MASK = 0x1C
ERROR_CODE_MASK = 0xFF00

# Field bit positions
ENABLE_POS = 0
READY_POS = 1
MODE_POS = 2
ERROR_CODE_POS = 8

# MODE field enumerated values
MODE_IDLE = 0
MODE_ACTIVE = 1
MODE_LOW_POWER = 2

def test_reset_value():
    """Test that CTRL_STATUS register reads reset value after device reset"""
    reset_device()
    value = read_register(CTRL_STATUS_ADDR)
    assert value == CTRL_STATUS_RESET_VALUE, f"Expected reset value {CTRL_STATUS_RESET_VALUE}, got {value}"

def test_enable_field_write_ones():
    """Test writing 1 to ENABLE field and reading back"""
    reset_device()
    write_register(CTRL_STATUS_ADDR, ENABLE_MASK)
    value = read_register(CTRL_STATUS_ADDR)
    assert (value & ENABLE_MASK) == ENABLE_MASK, f"ENABLE field should be 1, got {(value & ENABLE_MASK) >> ENABLE_POS}"

def test_enable_field_write_zeros():
    """Test writing 0 to ENABLE field and reading back"""
    reset_device()
    # First set the bit, then clear it
    write_register(CTRL_STATUS_ADDR, ENABLE_MASK)
    write_register(CTRL_STATUS_ADDR, 0)
    value = read_register(CTRL_STATUS_ADDR)
    assert (value & ENABLE_MASK) == 0, f"ENABLE field should be 0, got {(value & ENABLE_MASK) >> ENABLE_POS}"

def test_enable_field_isolation():
    """Test that writing to ENABLE field doesn't affect other fields"""
    reset_device()
    original_value = read_register(CTRL_STATUS_ADDR)
    write_register(CTRL_STATUS_ADDR, original_value | ENABLE_MASK)
    value = read_register(CTRL_STATUS_ADDR)
    other_fields = value & ~ENABLE_MASK
    original_other_fields = original_value & ~ENABLE_MASK
    assert other_fields == original_other_fields, f"Other fields changed when writing ENABLE"

def test_mode_field_write_ones():
    """Test writing all 1s to MODE field and reading back"""
    reset_device()
    write_register(CTRL_STATUS_ADDR, MODE_MASK)
    value = read_register(CTRL_STATUS_ADDR)
    expected_mode = MODE_MASK >> MODE_POS
    actual_mode = (value & MODE_MASK) >> MODE_POS
    assert actual_mode == expected_mode, f"MODE field should be {expected_mode}, got {actual_mode}"

def test_mode_field_write_zeros():
    """Test writing 0s to MODE field and reading back"""
    reset_device()
    # First set the bits, then clear them
    write_register(CTRL_STATUS_ADDR, MODE_MASK)
    write_register(CTRL_STATUS_ADDR, 0)
    value = read_register(CTRL_STATUS_ADDR)
    actual_mode = (value & MODE_MASK) >> MODE_POS
    assert actual_mode == 0, f"MODE field should be 0, got {actual_mode}"

def test_mode_field_isolation():
    """Test that writing to MODE field doesn't affect other fields"""
    reset_device()
    original_value = read_register(CTRL_STATUS_ADDR)
    write_register(CTRL_STATUS_ADDR, original_value | MODE_MASK)
    value = read_register(CTRL_STATUS_ADDR)
    other_fields = value & ~MODE_MASK
    original_other_fields = original_value & ~MODE_MASK
    assert other_fields == original_other_fields, f"Other fields changed when writing MODE"

def test_ready_field_read_only():
    """Test that READY field is read-only and cannot be modified"""
    reset_device()
    original_value = read_register(CTRL_STATUS_ADDR)
    original_ready = (original_value & READY_MASK) >> READY_POS
    
    # Try to write opposite value to READY field
    write_value = original_value ^ READY_MASK
    write_register(CTRL_STATUS_ADDR, write_value)
    
    new_value = read_register(CTRL_STATUS_ADDR)
    new_ready = (new_value & READY_MASK) >> READY_POS
    assert new_ready == original_ready, f"READY field changed from {original_ready} to {new_ready}, should be read-only"

def test_error_code_field_read_only():
    """Test that ERROR_CODE field is read-only and cannot be modified"""
    reset_device()
    original_value = read_register(CTRL_STATUS_ADDR)
    original_error_code = (original_value & ERROR_CODE_MASK) >> ERROR_CODE_POS
    
    # Try to write opposite value to ERROR_CODE field
    write_value = original_value ^ ERROR_CODE_MASK
    write_register(CTRL_STATUS_ADDR, write_value)
    
    new_value = read_register(CTRL_STATUS_ADDR)
    new_error_code = (new_value & ERROR_CODE_MASK) >> ERROR_CODE_POS
    assert new_error_code == original_error_code, f"ERROR_CODE field changed from {original_error_code} to {new_error_code}, should be read-only"

def test_enable_field_bit_position():
    """Test that ENABLE field is at correct bit position"""
    reset_device()
    write_register(CTRL_STATUS_ADDR, 1 << ENABLE_POS)
    value = read_register(CTRL_STATUS_ADDR)
    assert value & (1 << ENABLE_POS), f"ENABLE field not found at bit position {ENABLE_POS}"
    assert (value & ENABLE_MASK) == ENABLE_MASK, f"ENABLE field mask incorrect"

def test_ready_field_bit_position():
    """Test that READY field bit mask covers correct position"""
    # Since READY is read-only, we can only verify the mask position is correct
    expected_mask = 1 << READY_POS
    assert READY_MASK == expected_mask, f"READY mask {READY_MASK} should be {expected_mask}"

def test_mode_field_bit_position():
    """Test that MODE field is at correct bit positions"""
    reset_device()
    test_value = 0x7  # 3 bits set
    write_register(CTRL_STATUS_ADDR, test_value << MODE_POS)
    value = read_register(CTRL_STATUS_ADDR)
    extracted_mode = (value & MODE_MASK) >> MODE_POS
    assert extracted_mode == test_value, f"MODE field not at correct position, expected {test_value}, got {extracted_mode}"

def test_error_code_field_bit_position():
    """Test that ERROR_CODE field bit mask covers correct positions"""
    # Since ERROR_CODE is read-only, we can only verify the mask positions are correct
    expected_mask = 0xFF << ERROR_CODE_POS
    assert ERROR_CODE_MASK == expected_mask, f"ERROR_CODE mask {ERROR_CODE_MASK} should be {expected_mask}"

def test_mode_idle_value():
    """Test writing MODE_IDLE value to MODE field"""
    reset_device()
    write_register(CTRL_STATUS_ADDR, MODE_IDLE << MODE_POS)
    value = read_register(CTRL_STATUS_ADDR)
    actual_mode = (value & MODE_MASK) >> MODE_POS
    assert actual_mode == MODE_IDLE, f"MODE should be IDLE ({MODE_IDLE}), got {actual_mode}"

def test_mode_active_value():
    """Test writing MODE_ACTIVE value to MODE field"""
    reset_device()
    write_register(CTRL_STATUS_ADDR, MODE_ACTIVE << MODE_POS)
    value = read_register(CTRL_STATUS_ADDR)
    actual_mode = (value & MODE_MASK) >> MODE_POS
    assert actual_mode == MODE_ACTIVE, f"MODE should be ACTIVE ({MODE_ACTIVE}), got {actual_mode}"

def test_mode_low_power_value():
    """Test writing MODE_LOW_POWER value to MODE field"""
    reset_device()
    write_register(CTRL_STATUS_ADDR, MODE_LOW_POWER << MODE_POS)
    value = read_register(CTRL_STATUS_ADDR)
    actual_mode = (value & MODE_MASK) >> MODE_POS
    assert actual_mode == MODE_LOW_POWER, f"MODE should be LOW_POWER ({MODE_LOW_POWER}), got {actual_mode}"
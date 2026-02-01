# templates.py

GENERIC_TEST_TEMPLATE = """You are a test engineer. Given this function specification, 
generate pytest test cases that cover:
- Normal operation
- Edge cases  
- Error conditions

Specification:
{spec}

Output only valid Python pytest code."""

REGISTER_TEST_TEMPLATE = """You are a hardware validation engineer generating python tests for register access.

Given this register specification:
{spec}

Generate python tests that verify:

1. **Reset Value Test**: After reset, register reads the documented reset value

2. **RW Field Tests** (for each read-write field):
   - Write 1s to field, read back, verify value
   - Write 0s to field, read back, verify value
   - Verify writes don't affect other fields

3. **RO Field Tests** (for each read-only field):
   - Attempt write, verify field unchanged
   
4. **Bit Position Tests**:
   - Verify each field's bit mask is correct
   - Verify field values shift to correct positions

5. **Named Value Tests** (if field has enumerated values):
   - Write each named value, verify readback

Assume these helper functions exist:
- `read_register(address: int) -> int`
- `write_register(address: int, value: int) -> None`
- `reset_device() -> None`

Output only valid python code with descriptive test names.
Use constants for addresses and masks at the top of the file.
"""

INTERFACE_TEST_TEMPLATE = """You are a hardware validation engineer generating pytest tests.

Interface specification:
{spec}

Generate pytest tests covering:
1. Each operation with valid parameters
2. Error handling (NACK, timeout)
3. Boundary conditions (min/max sizes)

Assume helper functions: i2c_write(), i2c_read(), i2c_write_read(), i2c_probe(), reset_controller()

Output valid pytest code. Keep tests concise. Ensure all syntax is complete.
"""

TEMPLATES = {
    "generic": GENERIC_TEST_TEMPLATE,
    "register": REGISTER_TEST_TEMPLATE,
    "interface": INTERFACE_TEST_TEMPLATE,
}
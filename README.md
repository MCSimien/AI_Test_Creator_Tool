# Generate Tests

**AI-powered test generation for Python code and hardware validation**

Automatically generate comprehensive pytest test suites using Claude AI. Supports generic functions, hardware registers, and communication interfaces.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## Why Use This?

- **Save hours** writing boilerplate test code
- **Comprehensive coverage**: normal cases, edge cases, and error conditions
- **Multiple templates**: generic functions, hardware registers, I2C/SPI interfaces
- **Production-ready**: generates valid pytest code with proper assertions

---

## Quick Start

```bash
# Install dependencies
pip install anthropic python-dotenv

# Set your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Generate tests from a spec file
python cli.py specs/ctrl_status.yaml

# Or generate from inline specification
python cli.py -s "Function: add(a: int, b: int) -> int" --stdout
```

---

## Example Output

### Input Specification
```yaml
# specs/ctrl_status.yaml
register:
  name: CTRL_STATUS
  address: 0x1000
  width: 32
  reset_value: 0x00000000

  fields:
    - name: ENABLE
      bits: [0]
      access: RW
      description: "Enables the controller"
```

### Generated Test Code
```python
# generated_tests/test_ctrl_status.py
CTRL_STATUS_ADDR = 0x1000
ENABLE_MASK = 0x1

def test_reset_value():
    """Test that CTRL_STATUS register reads reset value after device reset"""
    reset_device()
    value = read_register(CTRL_STATUS_ADDR)
    assert value == 0x00000000

def test_enable_field_write_ones():
    """Test writing 1 to ENABLE field and reading back"""
    reset_device()
    write_register(CTRL_STATUS_ADDR, ENABLE_MASK)
    value = read_register(CTRL_STATUS_ADDR)
    assert (value & ENABLE_MASK) == ENABLE_MASK
```

**Result**: 20+ comprehensive tests generated in seconds, covering all register fields and access patterns.

---

## Project Structure

```
Generate_Tests/
├── Generate_Tests.py      # Core test generation engine
├── cli.py                 # Command-line interface
├── templates.py           # Test templates (generic, register, interface)
├── specs/                 # Example specification files
│   ├── checksum.txt       # Simple function spec
│   ├── ctrl_status.yaml   # Hardware register spec
│   └── i2c_bus.yaml       # Interface spec
└── generated_tests/       # Output directory for generated tests
    ├── test_checksum.py
    ├── test_ctrl_status.py
    └── test_i2c_bus.py
```

---

## Features

### Three Test Templates

**1. Generic Function Testing**
```bash
python cli.py -t generic specs/checksum.txt
```
- Normal operation tests
- Edge cases (empty input, max values, boundary conditions)
- Error handling (type errors, invalid inputs)

**2. Hardware Register Testing**
```bash
python cli.py -t register specs/ctrl_status.yaml
```
- Reset value verification
- RW field read/write tests
- RO field write protection
- Bit mask validation
- Field isolation tests

**3. Interface Testing**
```bash
python cli.py -t interface specs/i2c_bus.yaml
```
- Protocol operation tests
- Error handling (NACK, timeout)
- Boundary conditions (min/max sizes)

### CLI Options

```bash
python cli.py <spec_file>              # Auto-detect template from YAML
python cli.py -s "inline spec"         # Use inline specification
python cli.py -t register spec.yaml    # Force specific template
python cli.py -o custom_path.py        # Custom output path
python cli.py --stdout                 # Print to stdout
python cli.py --no-validate            # Skip syntax validation
```

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Generate_Tests
   ```

2. **Install dependencies**
   ```bash
   pip install anthropic python-dotenv
   ```

3. **Configure API key**
   ```bash
   echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
   ```

   Get your API key from: https://console.anthropic.com/

---

## Usage Examples

### Example 1: Generate Tests for a Function

**Input** (`specs/checksum.txt`):
```
Function: calculate_checksum(data: bytes) -> int

Calculates an 8-bit checksum by XORing all bytes together.
Returns 0 for empty input.
Raises TypeError if input is not bytes.
```

**Command**:
```bash
python cli.py specs/checksum.txt
```

**Output**: `generated_tests/test_checksum.py` with 25+ test cases

### Example 2: Quick Inline Test Generation

```bash
python cli.py -s "Function: parse_json(data: str) -> dict" --stdout
```

### Example 3: Custom Template and Output

```bash
python cli.py specs/i2c_bus.yaml -t interface -o tests/test_i2c.py
```

---

## Advanced Usage

### Python API

```python
from Generate_Tests import generate_tests, load_spec, save_tests

# Load specification from file
spec_content, template_type = load_spec("specs/ctrl_status.yaml")

# Generate tests
code = generate_tests(spec_content, template_type)

# Save to file
save_tests(code, "output/my_tests.py")
```

### Custom Templates

Edit `templates.py` to add your own test generation templates:

```python
CUSTOM_TEMPLATE = """Your custom prompt here..."""
TEMPLATES["custom"] = CUSTOM_TEMPLATE
```

---

## Configuration

**Model settings** (`Generate_Tests.py`):
```python
model = 'claude-sonnet-4-5-20250929'  # Claude model version
max_tokens = 2048                      # Max response length
```

**Template selection** (`templates.py`):
- `generic`: General Python functions
- `register`: Hardware register validation
- `interface`: Communication protocol testing

---

## Tips for Best Results

1. **Be specific in specifications**: Include types, return values, and exceptions
2. **Use YAML for complex specs**: Better structure for hardware/interface specs
3. **Review generated tests**: AI-generated code should be reviewed before use
4. **Iterate on prompts**: Modify templates for your specific use case

---

## File Descriptions

| File | Purpose |
|------|---------|
| `Generate_Tests.py` | Core AI test generation logic |
| `cli.py` | Command-line interface and argument parsing |
| `templates.py` | Test generation prompt templates |
| `specs/` | Example specification files |
| `generated_tests/` | Output directory for generated test files |
| `Generated_Tests_ID#.py` | Legacy output from direct script execution |
| `Generated_Tests_ID#-WithPrompt.txt` | Debug output with spec and tests |

---

## Requirements

- **Python**: 3.7+
- **API Key**: Anthropic API key (https://console.anthropic.com/)
- **Dependencies**:
  - `anthropic` - Claude API client
  - `python-dotenv` - Environment variable management

---

## License

MIT License - See LICENSE file for details

---

## Contributing

Contributions welcome! Areas for improvement:
- Additional test templates (timing, performance, security)
- Support for more specification formats (JSON, Protobuf)
- Test quality metrics and coverage analysis
- Integration with CI/CD pipelines

---

## Acknowledgments

Powered by [Claude AI](https://www.anthropic.com/claude) (Sonnet 4.5)

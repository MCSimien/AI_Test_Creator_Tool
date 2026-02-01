# Generate Tests

A Python utility that leverages Claude AI to automatically generate pytest test cases from function specifications.

## Overview

This tool uses Anthropic's Claude API to generate comprehensive pytest test cases based on function specifications. It automatically creates tests covering normal operation, edge cases, and error conditions.

## Features

- Generates pytest-compatible test code
- Covers multiple test scenarios:
  - Normal operation
  - Edge cases
  - Error conditions
- Outputs tests to both `.py` and `.txt` files
- Uses Claude Sonnet 4.5 for high-quality test generation

## Prerequisites

- Python 3.7+
- Anthropic API key
- Required packages:
  - `anthropic`
  - `python-dotenv`

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install anthropic python-dotenv
```

3. Create a `.env` file in the project directory and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

### As a Script

Run the script directly with the example specification:

```bash
python Generate_Tests.py
```

This will generate test cases for the example `calculate_checksum` function and save them to:
- `Generated_Tests_ID#.py` - Python test file
- `Generated_Tests_ID#-WithPrompt.txt` - Combined specification and tests

### As a Module

Import and use the `generate_tests` function in your own code:

```python
from Generate_Tests import generate_tests

spec = """
Function: my_function(param: str) -> int

Description of what the function does.
Include parameter types, return type, and any exceptions raised.
"""

tests = generate_tests(spec)
print(tests)
```

## Example

The script includes an example that generates tests for a checksum calculation function:

```python
spec = """
Function: calculate_checksum(data: bytes) -> int

Calculates an 8-bit checksum by XORing all bytes together.
Returns 0 for empty input.
Raises TypeError if input is not bytes.
"""

tests = generate_tests(spec)
```

## Output Files

- **Generated_Tests_ID#.py**: Contains only the generated pytest code, ready to run
- **Generated_Tests_ID#-WithPrompt.txt**: Contains both the original specification and generated tests for reference

## Configuration

The tool uses the following Claude API settings (in `Generate_Tests.py:21-24`):
- Model: `claude-sonnet-4-5-20250929`
- Max tokens: `2048`

You can modify these parameters in the `generate_tests` function to adjust output length or model version.

## Tips for Best Results

1. **Be specific**: Include parameter types, return types, and expected behaviors
2. **Document exceptions**: Specify what errors should be raised and when
3. **Describe edge cases**: Mention boundary conditions or special inputs
4. **Include examples**: Add sample inputs/outputs if helpful

## License

This project is provided as-is for educational and development purposes.

## Contributing

Feel free to submit issues or pull requests to improve the test generation quality or add new features.

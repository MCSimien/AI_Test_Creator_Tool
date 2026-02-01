# generator.py
import anthropic
import yaml
import ast
from pathlib import Path
from templates import TEMPLATES

def load_spec(spec_path: str) -> tuple[str, str]:
    """
    Load a spec file and return (content, detected_type).
    
    Returns:
        tuple: (spec_content as string, detected template type)
    """
    path = Path(spec_path)
    
    with open(path) as f:
        content = f.read()
    
    # Auto-detect type based on file extension and content
    if path.suffix in [".yaml", ".yml"]:
        parsed = yaml.safe_load(content)
        
        # Detect template type from YAML structure
        if "register" in parsed:
            return yaml.dump(parsed, default_flow_style=False), "register"
        elif "interface" in parsed:
            return yaml.dump(parsed, default_flow_style=False), "interface"
        else:
            # YAML but unknown structure, treat as generic
            return content, "generic"
    else:
        # Plain text file (.txt, .spec, etc.)
        return content, "generic"

def generate_tests(spec: str, template_type: str = "generic") -> str:
    """
    Generate tests using the appropriate template.
    
    Args:
        spec: The specification as a string
        template_type: One of "generic", "register", "interface"
    """
    if template_type not in TEMPLATES:
        raise ValueError(f"Unknown template type: {template_type}. "
                        f"Available: {list(TEMPLATES.keys())}")
    
    template = TEMPLATES[template_type]
    prompt = template.format(spec=spec)
    
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def generate_from_string(spec_text: str, template_type: str = "generic") -> str:
    """
    Generate tests directly from a string (no file needed).
    Useful for programmatic use or quick testing.
    """
    return generate_tests(spec_text, template_type)

def validate_syntax(code: str) -> tuple[bool, str]:
    """Check if generated code is valid Python."""
    code = code.strip()
    if code.startswith("```python"):
        code = code[9:]
    if code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    code = code.strip()
    
    try:
        ast.parse(code)
        return True, code
    except SyntaxError as e:
        return False, str(e)

def save_tests(code: str, output_path: str) -> None:
    """Save generated tests to file."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(code)

if __name__ == "__main__":
    # Example 1: Generic function spec (original use case)
    function_spec = """
    Function: calculate_checksum(data: bytes) -> int
    
    Calculates an 8-bit checksum by XORing all bytes together.
    Returns 0 for empty input.
    Raises TypeError if input is not bytes.
    """
    
    print("=== Generic Function Test ===")
    tests = generate_from_string(function_spec, "generic")
    print(tests)
    print()
    
    # Example 2: From YAML file (if it exists)
    spec_file = Path("specs/ctrl_status.yaml")
    if spec_file.exists():
        print("=== Register Test from YAML ===")
        spec_content, detected_type = load_spec(str(spec_file))
        tests = generate_tests(spec_content, detected_type)
        print(tests)
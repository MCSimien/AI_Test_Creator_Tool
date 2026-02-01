# cli.py
import argparse
import sys
from Generate_Tests import (
    load_spec, 
    generate_tests, 
    generate_from_string,
    validate_syntax, 
    save_tests
)
from templates import TEMPLATES

def main():
    parser = argparse.ArgumentParser(
        description="Generate hardware validation tests from specs"
    )
    
    # Input options (mutually exclusive: file or inline spec)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("spec_file", nargs="?", help="Path to spec file")
    input_group.add_argument("-s", "--spec", dest="inline_spec",
                             help="Inline specification string")
    
    parser.add_argument("-t", "--template", 
                        choices=list(TEMPLATES.keys()),
                        help="Template type (auto-detected for YAML files)")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("--stdout", action="store_true",
                        help="Print to stdout instead of file")
    parser.add_argument("--no-validate", action="store_true",
                        help="Skip syntax validation")
    
    args = parser.parse_args()
    
    # Get spec content and determine template type
    if args.inline_spec:
        spec_content = args.inline_spec
        template_type = args.template or "generic"
    else:
        spec_content, detected_type = load_spec(args.spec_file)
        template_type = args.template or detected_type
    
    print(f"Using template: {template_type}", file=sys.stderr)
    
    # Generate tests
    code = generate_tests(spec_content, template_type)
    
    # Validate syntax
    if not args.no_validate:
        is_valid, result = validate_syntax(code)
        if not is_valid:
            print(f"Syntax error in generated code: {result}", file=sys.stderr)
            sys.exit(1)
        code = result
    
    # Output
    if args.stdout:
        print(code)
    else:
        if args.output:
            output_path = args.output
        elif args.spec_file:
            spec_name = args.spec_file.split("/")[-1].replace(".yaml", "").replace(".txt", "")
            output_path = f"generated_tests/test_{spec_name}.py"
        else:
            output_path = "generated_tests/test_output.py"
        
        save_tests(code, output_path)
        print(f"Generated: {output_path}", file=sys.stderr)

if __name__ == "__main__":
    main()
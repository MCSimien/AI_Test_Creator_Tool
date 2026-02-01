from dotenv import load_dotenv
load_dotenv()

import anthropic

def generate_tests(function_spec: str) -> str:
    client = anthropic.Anthropic()

    prompt = f""" You are a senior test engineer. Given this function specification,
    generate pytest test cases that cover:

    - Normal operation
    - Edge cases
    - Error conditions

    Specification:
    {function_spec}

Output only valid Python pytest code."""
    
    message = client.messages.create(
        model='claude-sonnet-4-5-20250929',
        max_tokens=2048,
        messages=[{"role":"user", "content": prompt}]
    )

    return message.content[0].text

if __name__ == "__main__":
    spec = """
    Function: calculate_checksum(data: bytes) -> int
    
    Calculates an 8-bit checksum by XORing all bytes together.
    Returns 0 for empty input.
    Raises TypeError if input is not bytes.

"""

tests = generate_tests(spec)
print(tests)
with open('Generated_Tests_ID#-WithPrompt.txt', 'w') as f:
    f.writelines(spec)
    f.writelines(tests)

with open('Generated_Tests_ID#.py', 'w') as f:
    f.writelines(tests)


!pip install transformers torch huggingface_hub

import unittest
import torch
import ast
import re
from io import StringIO
from transformers import pipeline
from huggingface_hub import login

# Configuration
HF_TOKEN = token 
MODEL_NAME = "Salesforce/codegen-350M-mono" 

# Authenticate with Hugging Face
login(token=HF_TOKEN)

class CodeTestingTool:
    def __init__(self):
        # Initialize model pipeline
        self.test_gen = pipeline(
            'text-generation',
            model=MODEL_NAME,
            device=0 if torch.cuda.is_available() else -1,
            token=HF_TOKEN,
            torch_dtype=torch.float16,
            max_new_tokens=700
        )

    def generate_test_cases(self, code: str, max_retries=3):
        """Generate tests with error correction"""
        prompt = f"""Generate PROPERLY FORMATTED Python unit tests for:
{code}

STRICT RULES:
1. Class name: GeneratedTests(unittest.TestCase)
2. Exactly 3 test methods with docstrings
3. Perfect indentation and syntax
4. No markdown, only code
5. Complete import statements

EXAMPLE:
import unittest
class GeneratedTests(unittest.TestCase):
    def test_normal_case(self):
        \"\"\"Test addition with positive numbers\"\"\"
        self.assertEqual(add(2, 3), 5)

    def test_negative_numbers(self):
        \"\"\"Test addition with negative values\"\"\"
        self.assertEqual(add(-1, -1), -2)

    def test_mixed_types(self):
        \"\"\"Test type handling\"\"\"
        with self.assertRaises(TypeError):
            add("2", 3)

YOUR GENERATION:
"""
        for attempt in range(max_retries):
            try:
                response = self.test_gen(
                    prompt,
                    temperature=0.3,
                    do_sample=True,
                    truncation=True,
                    pad_token_id=50256
                )

                generated = response[0]['generated_text']
                test_code = self.clean_code(generated, prompt)

                if self.validate_syntax(test_code):
                    return test_code
                print(f"Retry {attempt+1}/{max_retries}...")

            except Exception as e:
                print(f"Generation error: {str(e)}")
                continue

        raise RuntimeError("Failed to generate valid code after retries")

    def clean_code(self, generated: str, prompt: str):
        """Extract and sanitize generated code"""
        # Remove prompt contamination
        code = generated.split("YOUR GENERATION:")[-1]

        # Fix common formatting issues
        code = re.sub(r'^```python\n?', '', code, flags=re.MULTILINE)
        code = re.sub(r'\n```$', '', code)
        code = code.replace('“', '"').replace('”', '"')

        # Ensure proper imports
        if 'import unittest' not in code:
            code = 'import unittest\n\n' + code

        # Fix indentation
        code = re.sub(r'^    ', '', code, flags=re.MULTILINE)

        return code.strip()

    def validate_syntax(self, code: str):
        """Validate code structure"""
        try:
            ast.parse(code)
            return True
        except SyntaxError as se:
            print(f"Syntax validation failed: {str(se)}")
            return False
        except Exception as e:
            print(f"Code validation error: {str(e)}")
            return False

    def test_generated_code(self, code: str):
        """Execute tests with comprehensive error handling"""
        try:
            test_code = self.generate_test_cases(code)
            print("\n" + "="*40)
            print("Generated Test Code:")
            print(test_code)
            print("="*40 + "\n")

            # Create isolated execution environment
            namespace = {
                '__name__': '__main__',
                'unittest': unittest,
                'self': self
            }

            # Execute generated code
            exec(test_code, namespace)

            # Configure test runner
            stream = StringIO()
            runner = unittest.TextTestRunner(
                stream=stream,
                verbosity=2,
                failfast=True
            )

            # Load and run tests
            test_class = namespace['GeneratedTests']
            suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
            result = runner.run(suite)

            # Display results
            print("\nTEST RESULTS:")
            print(stream.getvalue())

            return result.wasSuccessful()

        except KeyError:
            print("Error: GeneratedTests class not found in output")
            return False
        except SyntaxError as se:
            print(f"Critical syntax error: {str(se)}")
            return False
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return False

if __name__ == "__main__":
    # Example usage
    code_to_test = """
def add(a, b):
    return a + b
"""

    tester = CodeTestingTool()
    success = tester.test_generated_code(code_to_test)

    if success:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ TESTING FAILED")

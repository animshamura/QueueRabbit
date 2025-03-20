
# QueueRabbit

QueueRabbit is a Python utility that generates unit tests for a given Python function and runs the tests to ensure correctness. It utilizes the power of the Hugging Face model `Salesforce/codegen-350M-mono` for automatic code generation, and it integrates `unittest` for test execution.

## Features

- **Automated Test Generation**: Generate properly formatted Python unit tests using AI.
- **Flexible Configuration**: Retry the generation of tests multiple times to improve reliability.
- **Syntax Validation**: Automatically validate the generated code for syntax correctness before executing.
- **Test Execution**: Run generated unit tests and display results.
- **Error Handling**: Comprehensive error handling during the test generation and execution process.

## Prerequisites

To run **QueueRabbit**, you need to install the following dependencies:

- `transformers`
- `torch`
- `huggingface_hub`
- `unittest` (standard Python library)

You can install the necessary libraries using pip:

```bash
pip install transformers torch huggingface_hub
```

## Setup

1. **Hugging Face Token**: To authenticate with Hugging Face, you will need a Hugging Face account. You can obtain a token from [Hugging Face](https://huggingface.co/settings/tokens) and set it as the `HF_TOKEN` variable in the script.

2. **Model Selection**: The script uses the `Salesforce/codegen-350M-mono` model for test generation. You can change this model by updating the `MODEL_NAME` variable.

3. **CUDA Support**: If a GPU is available, the model will use it for faster processing. If you don't have a GPU, the script will fall back to CPU.

## Usage

1. Import the necessary modules and initialize the `QueueRabbit` class:
   ```python
   from token import token
   from QueueRabbit import QueueRabbit

   # Set your Hugging Face Token
   HF_TOKEN = token

   # Initialize the tester
   tester = QueueRabbit()
   ```

2. Provide the code you want to generate tests for and run the tests:
   ```python
   code_to_test = """
   def add(a, b):
       return a + b
   """

   success = tester.test_generated_code(code_to_test)

   if success:
       print("ALL TESTS PASSED!")
   else:
       print("TESTING FAILED")
   ```

3. **Test Generation**: The script will generate unit tests for the provided code based on the following rules:
   - Test cases should be formatted correctly using `unittest`.
   - Three test methods should be created with docstrings explaining their purpose.
   - Syntax errors in generated code will be caught and retried up to a maximum number of retries.

4. **Test Execution**: Once the test cases are generated, they will be executed using Python's built-in `unittest` framework, and the results will be printed.

## Example Output

```python
Generated Test Code:
import unittest

class GeneratedTests(unittest.TestCase):
    def test_normal_case(self):
        """Test addition with positive numbers"""
        self.assertEqual(add(2, 3), 5)

    def test_negative_numbers(self):
        """Test addition with negative values"""
        self.assertEqual(add(-1, -1), -2)

    def test_mixed_types(self):
        """Test type handling"""
        with self.assertRaises(TypeError):
            add("2", 3)
```

```bash
TEST RESULTS:
test_normal_case ... ok
test_negative_numbers ... ok
test_mixed_types ... FAIL

======================================================================
FAIL: test_mixed_types
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_script.py", line 20, in test_mixed_types
    self.assertRaises(TypeError, add, "2", 3)
AssertionError: TypeError not raised
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Hugging Face**: For providing pre-trained models and the `huggingface_hub` library.
- **Salesforce**: For the `codegen-350M-mono` model used for code generation.




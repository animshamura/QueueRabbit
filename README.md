

# **QueueRabbit**

QueueRabbit is an advanced Python utility that automates the generation of unit tests for Python functions. Using cutting-edge AI technology powered by Hugging Face's **Salesforce/codegen-350M-mono** model, QueueRabbit generates high-quality, formatted unit tests and runs them to ensure code correctness. It integrates seamlessly with Python’s built-in `unittest` framework, offering a robust and efficient testing solution.



## **Features**

- **Automated Test Generation**  
  Effortlessly generate properly formatted Python unit tests using AI-driven models.

- **Flexible Configuration**  
  Retry test generation automatically for better reliability, ensuring high-quality results.

- **Syntax Validation**  
  The tool validates generated code for syntax errors, allowing retries for clean, executable tests.

- **Comprehensive Test Execution**  
  Automatically run the generated unit tests and display the results.

- **Robust Error Handling**  
  Ensure smooth operation with intelligent error handling during code generation and test execution.



## **Prerequisites**

Before running QueueRabbit, ensure you have the following dependencies installed:

- `transformers`
- `torch`
- `huggingface_hub`
- `unittest` (included with Python)

To install the necessary dependencies, run the following command:

```bash
pip install transformers torch huggingface_hub
```



## **Setup Instructions**

1. **Obtain Hugging Face Token**  
   To authenticate with Hugging Face, sign up for an account and generate an access token from [Hugging Face](https://huggingface.co/settings/tokens).

2. **Update Token in Script**  
   Set the token in the script by updating the `HF_TOKEN` variable.

3. **Model Configuration**  
   By default, the script uses the **Salesforce/codegen-350M-mono** model. You can change this model by modifying the `MODEL_NAME` variable.

4. **CUDA Support**  
   QueueRabbit can utilize GPU for faster processing. If no GPU is available, it will fall back to CPU automatically.



## **How to Use QueueRabbit**

1. **Import the Necessary Modules**  
   Import the `QueueRabbit` class and your Hugging Face token.

   ```python
   from token import token
   from QueueRabbit import QueueRabbit

   # Set your Hugging Face Token
   HF_TOKEN = token

   # Initialize QueueRabbit
   tester = QueueRabbit()
   ```

2. **Provide the Code to Test**  
   Define the Python function you wish to generate tests for and run the tests.

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

3. **Test Generation Rules**  
   The generated tests will adhere to these key formatting rules:
   - **Proper indentation and syntax**.
   - **Three test methods** with descriptive docstrings.
   - **No markdown formatting**; only Python code.
   - **Complete import statements** for `unittest`.

4. **Test Execution**  
   Once tests are generated, they will be executed automatically using Python’s built-in `unittest` framework, and the results will be printed to the console.



## **Example Output**

**Generated Test Code:**

```python
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

**Test Results:**

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


## **License**

QueueRabbit is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.



## **Acknowledgments**

- **Hugging Face**: For providing the pre-trained models and the `huggingface_hub` library.
- **Salesforce**: For the powerful **codegen-350M-mono** model that drives test generation.


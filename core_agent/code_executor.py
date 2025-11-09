import json

def execute_code(code: str) -> dict:
    """
    Executes Python code in a restricted environment.

    Args:
        code: The Python code to execute.

    Returns:
        A dictionary containing the results of the execution, including
        any stdout, stderr, and the final result.
    """

    # A simple, restricted global environment
    restricted_globals = {
        "__builtins__": {
            "print": print,
            "range": range,
            "len": len,
            "str": str,
            "int": int,
            "float": float,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
            "abs": abs,
            "max": max,
            "min": min,
            "sum": sum,
            "sorted": sorted,
        }
    }

    # Redirect stdout to capture the output
    from io import StringIO
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()

    try:
        exec(code, restricted_globals)
        output = captured_output.getvalue()
        result = {"stdout": output, "stderr": "", "result": None}
    except Exception as e:
        output = captured_output.getvalue()
        result = {"stdout": output, "stderr": str(e), "result": None}
    finally:
        sys.stdout = old_stdout

    return result

# Example Usage:
if __name__ == '__main__':
    code_to_run = """
for i in range(5):
    print(f"Hello, World! {i}")
"""

    execution_result = execute_code(code_to_run)
    print(json.dumps(execution_result, indent=2))

    # Example of a failing execution
    failing_code = "print(undefined_variable)"
    execution_result = execute_code(failing_code)
    print(json.dumps(execution_result, indent=2))

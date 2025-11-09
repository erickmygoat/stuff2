import pytest
from core_agent.code_executor import execute_code

def test_code_executor_success():
    """Tests that the code executor can successfully execute a simple script."""
    code = "print('Hello, World!')"
    result = execute_code(code)
    assert result['stdout'] == 'Hello, World!\n'
    assert result['stderr'] == ''

def test_code_executor_failure():
    """Tests that the code executor correctly captures and reports errors."""
    code = "print(undefined_variable)"
    result = execute_code(code)
    assert "name 'undefined_variable' is not defined" in result['stderr']

def test_code_executor_restricted_environment():
    """Tests that the code executor's environment is properly restricted."""
    code = "import os"
    result = execute_code(code)
    assert "__import__ not found" in result['stderr']

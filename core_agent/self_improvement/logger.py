import time
import json

def performance_logger(func):
    """
    A decorator that logs the performance of a function.

    This logger captures key metrics such as execution time and the impact on the
    Core Objective Function (COF), storing them for later analysis by the
    Reflection Module.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The wrapper function.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        log_entry = {
            'timestamp': end_time,
            'function_name': func.__name__,
            'execution_time_ms': (end_time - start_time) * 1000,
            'cof_impact': result.get('cof_impact', None) if isinstance(result, dict) else None,
            'output_quality': result.get('quality', None) if isinstance(result, dict) else None,
        }

        # In a real system, this would write to a structured, persistent log store.
        with open('performance_logs.jsonl', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

        print(f"Logged performance for {func.__name__}: execution_time={(end_time - start_time) * 1000:.2f}ms")

        return result
    return wrapper

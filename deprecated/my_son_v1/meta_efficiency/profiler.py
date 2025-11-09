import cProfile
import pstats
import io
import time
import json

def internal_profiler(log_file='internal_performance.jsonl'):
    """
    A decorator that dynamically profiles agent modules to measure CPU cycles,
    memory allocation, and execution time for every function call.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            pr = cProfile.Profile()

            start_time = time.time()
            pr.enable()

            result = func(*args, **kwargs)

            pr.disable()
            end_time = time.time()

            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
            ps.print_stats(10) # Print top 10 offenders

            profiling_results = s.getvalue()

            log_entry = {
                'timestamp': end_time,
                'function_name': func.__name__,
                'execution_time_ms': (end_time - start_time) * 1000,
                'cpu_profile': {
                    'total_calls': ps.total_calls,
                    'total_tt': ps.total_tt,
                    'top_culprits': profiling_results
                }
            }

            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')

            return result
        return wrapper
    return decorator

# Example Usage:
@internal_profiler()
def example_inefficient_function():
    """An example of a function that could be optimized."""
    total = 0
    for i in range(1000000):
        total += i
    # A nested loop to simulate inefficiency
    for j in range(100):
        for k in range(100):
            pass
    return total

if __name__ == '__main__':
    print("--- Internal Profiler ---")
    print("Running an example inefficient function to generate a profile...")
    example_inefficient_function()
    print("Profiling complete. Data saved to 'internal_performance.jsonl'.")

    # Display the log content for verification
    with open('internal_performance.jsonl', 'r') as f:
        log = json.loads(f.readline())
        print("\n--- Generated Log Entry ---")
        print(json.dumps(log, indent=2))

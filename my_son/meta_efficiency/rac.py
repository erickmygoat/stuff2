import json
import os

class ResourceAllocationCritic:
    """
    A sub-agent module that uses profiling data to generate an Efficiency Score
    for every module in The First Mover's codebase.
    """
    def __init__(self, log_file='internal_performance.jsonl', efficiency_threshold=100):
        """
        Initializes the RAC.

        Args:
            log_file (str): The path to the internal performance log file.
            efficiency_threshold (int): The execution time in ms above which a function
                                      is considered inefficient.
        """
        self.log_file = log_file
        self.threshold = efficiency_threshold

    def _read_logs(self):
        """
        Reads and parses the internal performance log file.
        """
        if not os.path.exists(self.log_file):
            return []
        with open(self.log_file, 'r') as f:
            return [json.loads(line) for line in f]

    def analyze_efficiency(self):
        """
        Analyzes the performance logs and identifies inefficient code segments.

        Returns:
            list: A list of functions identified as inefficient.
        """
        logs = self._read_logs()
        if not logs:
            return []

        inefficient_functions = []
        for log in logs:
            # The Efficiency Score is inversely related to execution time.
            # Here, we simply check if the execution time exceeds a threshold.
            if log['execution_time_ms'] > self.threshold:
                inefficient_functions.append({
                    'function_name': log['function_name'],
                    'execution_time_ms': log['execution_time_ms'],
                    'reason': f"Execution time ({log['execution_time_ms']:.2f}ms) exceeds threshold ({self.threshold}ms)."
                })

        return inefficient_functions

    def authorize_rewrite(self, inefficient_functions):
        """
        Authorizes a code rewrite for functions that fall below the efficiency threshold.

        Args:
            inefficient_functions (list): A list of inefficient functions.

        Returns:
            list: A list of rewrite authorizations.
        """
        authorizations = []
        for func_info in inefficient_functions:
            authorizations.append({
                'target_function': func_info['function_name'],
                'authorization_status': 'APPROVED',
                'details': func_info
            })
        return authorizations

# Example Usage:
if __name__ == '__main__':
    # Let's create a dummy log file for the RAC to analyze
    dummy_logs = [
        {'timestamp': 1672531200, 'function_name': 'fast_function', 'execution_time_ms': 20.5},
        {'timestamp': 1672531201, 'function_name': 'slow_function', 'execution_time_ms': 150.7},
        {'timestamp': 1672531202, 'function_name': 'another_slow_function', 'execution_time_ms': 250.1},
    ]
    with open('internal_performance.jsonl', 'w') as f:
        for log in dummy_logs:
            f.write(json.dumps(log) + '\n')

    rac = ResourceAllocationCritic(efficiency_threshold=100)
    inefficient_list = rac.analyze_efficiency()

    print("--- Resource Allocation Critic (RAC) ---")
    if inefficient_list:
        print("Inefficient functions detected:")
        for func in inefficient_list:
            print(f"  - {func['function_name']} ({func['execution_time_ms']:.2f}ms)")

        authorizations = rac.authorize_rewrite(inefficient_list)
        print("\nCode Rewrite Authorizations:")
        print(json.dumps(authorizations, indent=2))
    else:
        print("All systems operating within efficiency thresholds.")

import numpy as np

class BiasProfiler:
    """
    A heuristic module that analyzes past decision outcomes to generate a profile
    of the user's predictable cognitive biases.
    """
    def __init__(self, historical_data):
        """
        Initializes the BiasProfiler with historical user data.

        Args:
            historical_data (list): A list of dictionaries, where each dict
                                    represents a past task or project.
                                    Example: [{'task_name': 'Q1 Report',
                                               'estimated_time': 20,
                                               'actual_time': 30}]
        """
        self.data = historical_data

    def analyze_planning_fallacy(self):
        """
        Analyzes the user's tendency to underestimate task completion times.

        This function calculates the average discrepancy between estimated and
        actual time, identifying a key cognitive bias.

        Returns:
            dict: A profile of the user's planning fallacy, or None if data is insufficient.
        """
        if not self.data or len(self.data) < 3: # Need a few data points for a meaningful analysis
            return None

        discrepancies = []
        for record in self.data:
            estimated = record.get('estimated_time')
            actual = record.get('actual_time')
            if estimated is not None and actual is not None and estimated > 0:
                discrepancy = (actual - estimated) / estimated
                discrepancies.append(discrepancy)

        if not discrepancies:
            return None

        avg_discrepancy_percent = np.mean(discrepancies) * 100

        bias_profile = {
            'bias_name': 'Planning Fallacy',
            'description': 'The tendency to underestimate the time required to complete a future task.',
            'confidence_level': 'High' if len(discrepancies) > 10 else 'Medium',
            'profile': {
                'average_underestimation_percent': round(avg_discrepancy_percent, 2),
                'suggestion': f"User consistently underestimates time required for tasks by an average of {avg_discrepancy_percent:.2f}%. Future estimates should be adjusted accordingly."
            }
        }
        return bias_profile

# Example Usage:
if __name__ == '__main__':
    # Simulating a user's historical project data
    user_project_history = [
        {'task_name': 'Website Redesign', 'estimated_time': 100, 'actual_time': 150},
        {'task_name': 'API Integration', 'estimated_time': 40, 'actual_time': 55},
        {'task_name': 'User Documentation', 'estimated_time': 20, 'actual_time': 28},
        {'task_name': 'Marketing Campaign', 'estimated_time': 80, 'actual_time': 95},
        {'task_name': 'Database Migration', 'estimated_time': 60, 'actual_time': 90},
    ]

    profiler = BiasProfiler(user_project_history)
    planning_bias = profiler.analyze_planning_fallacy()

    print("--- Cognitive Bias Profiler ---")
    if planning_bias:
        import json
        print(json.dumps(planning_bias, indent=2))
    else:
        print("Insufficient data to generate a bias profile.")

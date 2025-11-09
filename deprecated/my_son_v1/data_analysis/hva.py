

class HVAPrioritization:
    """
    A module for identifying High-Value Activities (HVAs) by assigning an
    Impact Score to every potential user action.
    """
    def __init__(self, weights):
        """
        Initializes the HVA Prioritization module with a set of weights.

        Args:
            weights (dict): A dictionary of weights for different scoring dimensions.
                            Example: {'goal_alignment': 0.4, 'urgency': 0.2,
                                      'skill_development': 0.1, 'strategic_importance': 0.3}
        """
        if not abs(sum(weights.values()) - 1.0) < 1e-9:
            raise ValueError("The sum of weights must be 1.")
        self.weights = weights

    def calculate_impact_score(self, task):
        """
        Calculates a weighted Impact Score for a given task.

        The score quantifies the task's potential to maximize the user's COF.

        Args:
            task (dict): A dictionary representing a task, with scores for each
                         dimension (e.g., 'goal_alignment', 'urgency'). Scores
                         should be normalized from 0 to 1.

        Returns:
            float: The calculated Impact Score for the task.
        """
        score = 0
        for dimension, weight in self.weights.items():
            score += task.get(dimension, 0) * weight
        return score

    def prioritize_tasks(self, tasks):
        """
        Ranks a list of tasks based on their Impact Score.

        Args:
            tasks (list): A list of task dictionaries.

        Returns:
            list: The list of tasks, sorted by Impact Score in descending order.
        """
        for task in tasks:
            task['impact_score'] = self.calculate_impact_score(task)

        return sorted(tasks, key=lambda x: x['impact_score'], reverse=True)

# Example Usage:
if __name__ == '__main__':
    # Defining the user's strategic priorities
    user_weights = {
        'goal_alignment': 0.4,       # How well the task aligns with Q4 goals
        'urgency': 0.2,              # Deadlines and time-sensitivity
        'skill_development': 0.1,    # Opportunity to learn a new skill
        'strategic_importance': 0.3  # Long-term impact on career/business
    }

    # Simulating a user's to-do list
    user_tasks = [
        {'name': 'Finalize Q4 Budget', 'goal_alignment': 0.9, 'urgency': 0.8, 'skill_development': 0.1, 'strategic_importance': 0.7},
        {'name': 'Learn new CRM software', 'goal_alignment': 0.3, 'urgency': 0.2, 'skill_development': 0.9, 'strategic_importance': 0.6},
        {'name': 'Schedule team offsite', 'goal_alignment': 0.5, 'urgency': 0.6, 'skill_development': 0.2, 'strategic_importance': 0.4},
        {'name': 'Draft investor update', 'goal_alignment': 0.8, 'urgency': 0.9, 'skill_development': 0.3, 'strategic_importance': 0.9},
    ]

    prioritizer = HVAPrioritization(user_weights)
    ranked_tasks = prioritizer.prioritize_tasks(user_tasks)

    print("--- HVA Prioritization ---")
    print("User's Prioritized Directives for Today:")
    for i, task in enumerate(ranked_tasks):
        print(f"{i+1}. {task['name']} (Impact Score: {task['impact_score']:.2f})")

    print(f"\nThe top-ranked HVA is '{ranked_tasks[0]['name']}', which should be the user's primary focus.")

# In a real-world scenario, these weights would be fine-tuned based on user priorities.
COF_WEIGHTS = {
    'goal_attainment': 0.5,
    'efficiency': 0.3,
    'time_saved': 0.2,
}

def calculate_cof(goal_attainment, efficiency_metrics, time_to_completion):
    """
    Calculates the Core Objective Function (COF) score.

    The COF is a mathematical function that quantifies user progress toward stated goals.
    This implementation uses a weighted sum of key performance indicators.

    Args:
        goal_attainment (float): A score from 0 to 1 representing the degree of goal completion.
        efficiency_metrics (float): A score from 0 to 1 representing the efficiency of task execution.
        time_to_completion (float): A metric representing the time saved or taken, normalized for COF calculation.

    Returns:
        float: The calculated COF score.
    """
    cof_score = (
        COF_WEIGHTS['goal_attainment'] * goal_attainment +
        COF_WEIGHTS['efficiency'] * efficiency_metrics +
        COF_WEIGHTS['time_saved'] * time_to_completion
    )
    return cof_score

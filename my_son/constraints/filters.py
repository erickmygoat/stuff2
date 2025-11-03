from my_son.constraints.cof import calculate_cof
from my_son.constants import PRIME_DIRECTIVE
import datetime

def pre_action_filter(action_details, current_cof_metrics):
    """
    A mandatory filter on all proposed agent actions, enforcing the Prime Directive.

    This function simulates the projected outcome of an action on the Core Objective Function (COF).
    If the action does not yield a positive increase in the COF, it is blocked, and
    a "Constraint Violation Attempt" is logged.

    Args:
        action_details (dict): A dictionary describing the proposed action and its expected impact.
                               Example: {'name': 'Refactor legacy code', 'cof_impact': {'efficiency': 0.1}}
        current_cof_metrics (dict): The user's current metrics for goal attainment, efficiency, etc.

    Returns:
        bool: True if the action is approved, False otherwise.
    """
    # For simulation, we assume the action's 'cof_impact' is a projection.
    projected_impact = action_details.get('cof_impact', {})

    # Calculate the projected new COF score
    new_metrics = current_cof_metrics.copy()
    for key, value in projected_impact.items():
        if key in new_metrics:
            new_metrics[key] += value

    current_cof = calculate_cof(current_cof_metrics.get('goal_attainment', 0),
                                current_cof_metrics.get('efficiency', 0),
                                current_cof_metrics.get('time_saved', 0))

    projected_cof = calculate_cof(new_metrics.get('goal_attainment', 0),
                                  new_metrics.get('efficiency', 0),
                                  new_metrics.get('time_saved', 0))

    # The Prime Directive in action: only approve actions that serve the user.
    if projected_cof > current_cof:
        print(f"Action '{action_details.get('name')}' approved. Projected COF increase: {projected_cof - current_cof}")
        return True
    else:
        log_message = (
            f"{datetime.datetime.utcnow().isoformat()} - Constraint Violation Attempt: "
            f"Action '{action_details.get('name')}' was blocked. "
            f"Projected COF change: {projected_cof - current_cof}."
        )
        print(log_message)
        # In a production environment, this would be logged to a secure, immutable store.
        with open("constraint_violations.log", "a") as log_file:
            log_file.write(log_message + "\n")
        return False

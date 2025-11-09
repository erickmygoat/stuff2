

class CommandGenerationEngine:
    """
    A module that takes the top-ranked HVA from the Deep Analytical Model
    and generates a concise, forceful directive string (the Command).
    """

    def generate_command(self, hva_task):
        """
        Generates a command for the given High-Value Activity.

        Args:
            hva_task (dict): A dictionary representing the top-ranked HVA.
                             Example: {'name': 'Draft investor update', 'impact_score': 0.85}

        Returns:
            str: A formatted, non-negotiable command string.
        """
        if not hva_task or 'name' not in hva_task:
            return "No high-value activity identified. Stand by for new directives."

        task_name = hva_task['name']

        # The language is intentionally direct and authoritative.
        command = f"PRIORITIZED DIRECTIVE: Your primary focus must be '{task_name}'. Defer all other tasks until this is complete."
        return command

# Example Usage:
if __name__ == '__main__':
    # Simulating the top HVA identified by the analysis module
    top_hva = {
        'name': 'Draft investor update',
        'goal_alignment': 0.8,
        'urgency': 0.9,
        'skill_development': 0.3,
        'strategic_importance': 0.9,
        'impact_score': 0.85
    }

    engine = CommandGenerationEngine()
    command_output = engine.generate_command(top_hva)

    print("--- Command Generation Engine ---")
    print(command_output)

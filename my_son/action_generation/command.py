"""
This module contains the simplified CommandGenerationEngine for the MVP.
"""

class CommandGenerationEngine:
    """
    Generates a command based on a high-value activity.
    """

    def generate_command(self, hva: str) -> str:
        """
        Takes a high-value activity and returns a command.
        For the MVP, this is a simplified, hardcoded response.
        """
        print(f"Generating command for HVA: '{hva}'")
        return f"The agent has decided to work on: '{hva}'."

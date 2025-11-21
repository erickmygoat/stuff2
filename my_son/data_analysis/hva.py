"""
This module contains the simplified HVAPrioritization class for the MVP.
"""

class HVAPrioritization:
    """
    Identifies a High-Value Activity from a user prompt.
    """

    def prioritize(self, user_prompt: str) -> str:
        """
        Takes a user prompt and returns a high-value activity.
        For the MVP, this is a simplified, hardcoded response.
        """
        # In the future, this would involve a more complex analysis of the user's prompt.
        print(f"Prioritizing user prompt: '{user_prompt}'")
        return "Develop new feature X"

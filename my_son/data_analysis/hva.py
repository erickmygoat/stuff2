"""
This module contains the HVAPrioritization class using an LLM.
"""
from my_son.agent.llm import LLMClient

class HVAPrioritization:
    """
    Identifies a High-Value Activity from a user prompt using an LLM.
    """

    def __init__(self):
        self.llm = LLMClient()

    def prioritize(self, user_prompt: str) -> str:
        """
        Takes a user prompt and returns a high-value activity identified by the LLM.
        """
        print(f"Prioritizing user prompt: '{user_prompt}'")

        system_prompt = (
            "You are an expert project manager and strategist. "
            "Analyze the user's request and identify the single most High-Value Activity (HVA) "
            "that the agent should perform. Return only the HVA as a concise string."
        )

        hva = self.llm.complete(user_prompt, system_prompt=system_prompt)
        return hva

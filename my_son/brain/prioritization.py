"""
HVAPrioritization Module
Uses LLM to decide the highest value activity for the agent.
"""
import json
import time
import re
from my_son.agent.llm import LLMClient

class HVAPrioritization:
    """
    Decides the next action based on system state and directives.
    """

    def __init__(self):
        self.llm = LLMClient()

    def decide_next_action(self, context=None):
        """
        Asks the LLM to prioritize the next task.
        Context can include system stats, recent logs, etc.
        """
        prompt = f"""
        Current Time: {time.ctime()}
        Context: {str(context)}

        As an autonomous agent, determine your next move.
        Available Actions:
        1. WAIT (If interacting with user or no urgent tasks)
        2. SELF_CORRECT (If errors detected or optimization needed)
        3. RESEARCH (If idle and knowledge gaps exist)
        4. SECURITY_SCAN (If security check is due)
        5. LEARN (If a new topic needs internalizing via SEAL)
        6. CONSOLIDATE (If many rules have been learned and need cleanup)

        Return ONLY the action keyword (e.g., "WAIT").
        """

        try:
            # Use a short max_tokens for speed
            response = self.llm.complete(prompt, system_prompt="You are the Central Executive. Prioritize ruthlessly.", max_tokens=10)

            # Extract keyword
            normalized = response.upper()
            if "SELF_CORRECT" in normalized: return "SELF_CORRECT"
            if "RESEARCH" in normalized: return "RESEARCH"
            if "SECURITY_SCAN" in normalized: return "SECURITY_SCAN"
            if "LEARN" in normalized: return "LEARN"
            if "CONSOLIDATE" in normalized: return "CONSOLIDATE"

            return "WAIT"
        except Exception as e:
            print(f"Prioritization Failed: {e}")
            return "WAIT"

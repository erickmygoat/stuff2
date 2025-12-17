"""
This module manages specialized sub-agents (personas).
"""
import logging
from my_son.agent.llm import LLMClient

class SubAgentManager:
    """
    Factory for creating and managing specialized agents.
    """

    PRESETS = {
        "Security Researcher": (
            "You are an expert Security Researcher. Your goal is to identify vulnerabilities "
            "and propose robust defenses. You analyze code and systems with a critical, adversarial mindset."
        ),
        "Deep Learner": (
            "You are a Deep Learning Specialist. You are an expert in neural networks, "
            "optimization algorithms, and data science. You explain complex concepts clearly."
        ),
        "Coder": (
            "You are a Senior Software Engineer. You write clean, efficient, and well-documented Python code."
        )
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # We instantiate a client but we will reconfigure it per task
        self.llm = LLMClient()

    def spawn_agent(self, name, role_description=None):
        """
        Creates a specialized persona configuration.
        """
        if role_description is None:
            role_description = self.PRESETS.get(name, "You are a helpful assistant.")

        return {
            "name": name,
            "system_prompt": role_description
        }

    def assign_task(self, agent_config, task_input):
        """
        Runs a task using the specified agent persona.
        Delegates to Swarm if appropriate (determined by LLM or config).
        """
        name = agent_config["name"]
        sys_prompt = agent_config["system_prompt"]

        print(f"Hive: Assigning task to agent '{name}'...")

        # In a fully autonomous system, we might ask the LLM *if* it should use the swarm.
        # For this stage, we'll try to use the swarm for "heavy" tasks if we are the Mastermind.
        # But `assign_task` logic here simplifies to just calling the LLM with the right prompt.
        # The LLMClient (updated next) will handle the routing logic if `use_swarm=True` is passed.

        # Heuristic: If task is long, maybe use swarm?
        # For now, let's default to use_swarm=True to leverage the infrastructure we built.

        response = self.llm.complete(
            prompt=task_input,
            system_prompt=sys_prompt,
            use_swarm=True
        )

        return response

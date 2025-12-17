import asyncio
import time
import json
import os
from my_son.agent.agent import Agent
from my_son.agent.llm import LLMClient

class ConversationalEngine:
    """
    Manages the conversational flow using a local LLM and Memory.
    """

    def __init__(self, agent: Agent, log_file="performance.jsonl"):
        """
        Initializes the conversational engine.
        """
        self.agent = agent
        self.llm = LLMClient()
        self.log_file = log_file

    async def handle_user_input(self, user_input: str) -> str:
        """
        Handles a single turn of the conversation, returning the response directly.

        :param user_input: The input from the user.
        :return: The agent's response.
        """
        start_time = time.time()
        print(f"ConversationalEngine: Received user input: {user_input}")

        # 1. Generate Response using Local LLM (Context handling is inside LLMClient.complete)
        response = self.llm.complete(user_input, system_prompt=self.agent.get_prompt())

        total_duration = time.time() - start_time

        print(f"ConversationalEngine: Generated response: {response}")

        # Log performance
        self._log_performance({
            "input": user_input,
            "response": response,
            "latency": total_duration,
            "timestamp": time.time()
        })

        return response

    def _log_performance(self, log_entry):
        """
        Logs performance metrics to a JSONL file.
        """
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

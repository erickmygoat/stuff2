import asyncio
import time
import json
import os
from my_son.agent.agent import Agent
from my_son.data_analysis.hva import HVAPrioritization
from my_son.action_generation.command import CommandGenerationEngine

class ConversationalEngine:
    """
    Manages the conversational flow with the user, leveraging advanced prompting techniques.
    """

    def __init__(self, agent: Agent, log_file="performance.jsonl"):
        """
        Initializes the conversational engine.

        :param agent: The main agent instance.
        :param log_file: The file to log performance metrics to.
        """
        self.agent = agent
        self.hva_prioritizer = HVAPrioritization()
        self.command_generator = CommandGenerationEngine()
        self.log_file = log_file

    async def start_conversation(self):
        """
        Starts the main conversational loop.
        """
        print("ConversationalEngine: Starting conversation.")
        user_input = await self.get_user_input()
        if user_input:
            await self.handle_user_input(user_input)
        print("ConversationalEngine: Conversation ended.")

    async def get_user_input(self):
        """
        Gets input from the user from input.txt and clears it.
        """
        if not os.path.exists("input.txt"):
             return None

        content = None
        with open("input.txt", "r") as f:
            content = f.read().strip()

        if content:
            # Clear the file to avoid processing the same input indefinitely
            with open("input.txt", "w") as f:
                f.write("")

        return content

    async def handle_user_input(self, user_input: str):
        """
        Handles a single turn of the conversation.

        :param user_input: The input from the user.
        """
        start_time = time.time()
        print(f"ConversationalEngine: Received user input: {user_input}")

        # 1. Prioritize the user input to get a high-value activity.
        hva_start = time.time()
        hva = self.hva_prioritizer.prioritize(user_input)
        hva_duration = time.time() - hva_start

        # 2. Generate a command based on the high-value activity.
        cmd_start = time.time()
        command = self.command_generator.generate_command(hva)
        cmd_duration = time.time() - cmd_start

        total_duration = time.time() - start_time

        print(f"ConversationalEngine: Generated response: {command}")

        # Write the response to output.txt
        with open("output.txt", "w") as f:
            f.write(command)
        print(f"Agent response written to output.txt")

        # Log performance
        self._log_performance({
            "input": user_input,
            "hva": hva,
            "response": command,
            "hva_latency": hva_duration,
            "command_latency": cmd_duration,
            "total_latency": total_duration,
            "timestamp": time.time()
        })

    def _log_performance(self, log_entry):
        """
        Logs performance metrics to a JSONL file.
        """
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

import asyncio
from my_son.agent.agent import Agent
from my_son.data_analysis.hva import HVAPrioritization
from my_son.action_generation.command import CommandGenerationEngine

class ConversationalEngine:
    """
    Manages the conversational flow with the user, leveraging advanced prompting techniques.
    """

    def __init__(self, agent: Agent):
        """
        Initializes the conversational engine.

        :param agent: The main agent instance.
        """
        self.agent = agent
        self.hva_prioritizer = HVAPrioritization()
        self.command_generator = CommandGenerationEngine()

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
        Gets input from the user from input.txt.
        """
        with open("input.txt", "r") as f:
            return f.read().strip()

    async def handle_user_input(self, user_input: str):
        """
        Handles a single turn of the conversation.

        :param user_input: The input from the user.
        """
        print(f"ConversationalEngine: Received user input: {user_input}")

        # 1. Prioritize the user input to get a high-value activity.
        hva = self.hva_prioritizer.prioritize(user_input)

        # 2. Generate a command based on the high-value activity.
        command = self.command_generator.generate_command(hva)

        print(f"ConversationalEngine: Generated response: {command}")

        # Write the response to output.txt
        with open("output.txt", "w") as f:
            f.write(command)
        print(f"Agent response written to output.txt")

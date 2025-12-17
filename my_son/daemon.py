import asyncio
import time
from my_son.agent.agent import Agent
from my_son.firebase.firebase_client import FirebaseClient
from my_son.conversational.conversational_engine import ConversationalEngine
from my_son.self_improvement.reflection import ReflectionModule
from my_son.self_improvement.code_modification import CodeModificationModule
from my_son.self_improvement.deployment import DeploymentModule

class AutonomousAgentDaemon:
    """
    Orchestrates the main loop and the self-improvement cycle.
    """

    def __init__(self):
        # Initialize dependencies
        # For MVP, using default/placeholder user_id and mock client if keys missing
        self.firebase_client = FirebaseClient()
        self.agent = Agent(user_id="default_user", firebase_client=self.firebase_client)

        self.conversational_engine = ConversationalEngine(self.agent)
        self.reflection_module = ReflectionModule()
        self.code_modification_module = CodeModificationModule()
        self.deployment_module = DeploymentModule()

    async def run_loop(self):
        """
        Runs the main loop: Conversation -> Reflection -> Self-Correction.
        """
        print("Starting Autonomous Agent Daemon...")
        while True:
            # 1. Run Conversation / User Interaction
            await self.conversational_engine.start_conversation()

            # 2. Run Self-Improvement Cycle
            self.run_self_improvement()

            # Sleep briefly to avoid busy loop if no input
            await asyncio.sleep(5)

    def run_self_improvement(self):
        """
        Executes the self-improvement pipeline.
        """
        print("Daemon: Initiating self-improvement check...")

        # A. Reflection
        plan = self.reflection_module.run_reflection_cycle()
        if not plan:
            print("Daemon: No self-correction plan generated.")
            return

        # B. Code Modification
        print(f"Daemon: Plan found. Generating patch...")
        patch = self.code_modification_module.generate_patch(plan)
        if not patch:
            print("Daemon: No patch generated.")
            return

        # C. Deployment
        print(f"Daemon: Patch generated. Attempting deployment...")
        success = self.deployment_module.apply_patch(patch)

        if success:
            print("Daemon: Self-improvement cycle completed successfully.")
        else:
            print("Daemon: Deployment failed.")

if __name__ == "__main__":
    daemon = AutonomousAgentDaemon()
    asyncio.run(daemon.run_loop())

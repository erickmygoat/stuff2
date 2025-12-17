import asyncio
import time
from my_son.agent.agent import Agent
from my_son.firebase.firebase_client import FirebaseClient
from my_son.conversational.conversational_engine import ConversationalEngine
from my_son.self_improvement.reflection import ReflectionModule
from my_son.self_improvement.code_modification import CodeModificationModule
from my_son.self_improvement.deployment import DeploymentModule
from my_son.sync.sync_manager import SyncManager
from my_son.interface.voice import VoiceInterface
from my_son.interface.state import state_manager
from my_son.agent.scheduler import Scheduler
from my_son.self_improvement.debugger import AutoDoctor
from my_son.config import DEBUG_MODE

class AutonomousAgentDaemon:
    """
    Orchestrates the main loop and the self-improvement cycle.
    """

    def __init__(self):
        # Initialize dependencies
        self.firebase_client = FirebaseClient()
        self.agent = Agent(user_id="default_user", firebase_client=self.firebase_client)

        self.conversational_engine = ConversationalEngine(self.agent)
        self.reflection_module = ReflectionModule()
        self.code_modification_module = CodeModificationModule()
        self.deployment_module = DeploymentModule()

        self.sync_manager = SyncManager(agent_id="agent_v1", firebase_client=self.firebase_client)
        self.voice_interface = VoiceInterface()
        self.scheduler = Scheduler()
        self.debugger = AutoDoctor()

    async def run_loop(self):
        """
        Runs the main loop: Conversation -> Reflection -> Self-Correction.
        """
        print("Starting Autonomous Agent Daemon...")
        await state_manager.log_activity("Daemon started.")

        # Start Scheduler & Debugger
        self.scheduler.start()
        if DEBUG_MODE:
            # Run monitor in thread (it blocks, so needs thread or async wrapper)
            # Since monitor_logs is blocking, we should launch it carefully.
            # Ideally AutoDoctor.monitor_logs should be threaded internally or here.
            import threading
            threading.Thread(target=self.debugger.monitor_logs, daemon=True).start()
            await state_manager.log_activity("Auto-Doctor enabled.")

        while True:
            # Update System Stats
            await state_manager.update_state("system_stats", state_manager.get_system_stats())

            # 0. Sync Heartbeat
            self.sync_manager.send_heartbeat()

            # 1. Run Conversation / User Interaction
            # Note: ConversationalEngine is now mostly reactive via API,
            # but start_conversation checks for legacy input file.
            # We can keep it or remove it. Let's keep it for file-based compat.
            await self.conversational_engine.start_conversation()

            # 2. Run Self-Improvement Cycle
            self.run_self_improvement()

            # Sleep briefly to avoid busy loop
            await asyncio.sleep(5)

    def run_self_improvement(self):
        """
        Executes the self-improvement pipeline.
        """
        # A. Reflection
        plan = self.reflection_module.run_reflection_cycle()
        if not plan:
            return

        state_manager.update_state_sync = lambda k, v: asyncio.create_task(state_manager.update_state(k, v)) # Hack for sync context
        asyncio.create_task(state_manager.log_activity("Self-Correction Plan generated."))

        # B. Code Modification
        asyncio.create_task(state_manager.update_state("current_task", "Self-Improving"))
        patch = self.code_modification_module.generate_patch(plan)
        if not patch:
            return

        # C. Deployment
        asyncio.create_task(state_manager.log_activity("Deploying patch..."))
        success = self.deployment_module.apply_patch(patch)

        if success:
            asyncio.create_task(state_manager.log_activity("Self-improvement successful."))
            self.voice_interface.speak("I have upgraded my code.")
        else:
            asyncio.create_task(state_manager.log_activity("Deployment failed."))

        asyncio.create_task(state_manager.update_state("current_task", "Idle"))

if __name__ == "__main__":
    daemon = AutonomousAgentDaemon()
    asyncio.run(daemon.run_loop())

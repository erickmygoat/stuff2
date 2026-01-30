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
from my_son.security.researcher import SecurityResearcher
from my_son.brain.deep_learner import DeepLearner
from my_son.brain.prioritization import HVAPrioritization
from my_son.learning.seal import SEALEngine
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
        self.security = SecurityResearcher()
        self.learner = DeepLearner()
        self.prioritizer = HVAPrioritization()
        self.seal_engine = SEALEngine()
        self.last_decision_time = 0

        # Schedule Default Autonomous Tasks immediately (Fallback/Guaranteed tasks)
        self._schedule_default_tasks()

    async def run_loop(self):
        """
        Runs the main loop: Conversation -> Reflection -> Self-Correction.
        """
        print("Starting Autonomous Agent Daemon: My Son is Alive.")
        self.loop = asyncio.get_running_loop()
        await state_manager.log_activity("My Son is Alive. Daemon started.")

        # Start Scheduler & Debugger
        self.scheduler.start()
        if DEBUG_MODE:
            import threading
            threading.Thread(target=self.debugger.monitor_logs, daemon=True).start()
            await state_manager.log_activity("Auto-Doctor enabled.")

        while True:
            # Update System Stats
            await state_manager.update_state("system_stats", state_manager.get_system_stats())

            # 0. Sync Heartbeat
            self.sync_manager.send_heartbeat()

            # 1. Run Conversation / User Interaction
            await self.conversational_engine.start_conversation()

            # 2. Autonomous Prioritization (Every 30s)
            if time.time() - self.last_decision_time > 30:
                self.last_decision_time = time.time()
                action = await asyncio.to_thread(self.prioritizer.decide_next_action, {"stats": state_manager.get_system_stats()})

                if action != "WAIT":
                    await state_manager.log_activity(f"Brain: Decided to {action}...")

                if action == "SELF_CORRECT":
                    await asyncio.to_thread(self.run_self_improvement)
                elif action == "RESEARCH" or action == "LEARN":
                    await asyncio.to_thread(self._autonomous_research)
                elif action == "CONSOLIDATE":
                    await state_manager.log_activity("Brain: Consolidating Knowledge...")
                    await asyncio.to_thread(self.seal_engine.consolidate_knowledge)
                elif action == "SECURITY_SCAN":
                    await asyncio.to_thread(self._autonomous_security_scan)

            # Sleep briefly to avoid busy loop
            await asyncio.sleep(5)

    def _schedule_default_tasks(self):
        """
        Registers autonomous tasks to the scheduler.
        """
        # 1. Security Scan (Every 60 minutes)
        # We need a dummy code snippet or path to scan. For now, scan self.
        self.scheduler.add_recurring_task(60, self._autonomous_security_scan)

        # 2. Deep Research (Every 24 hours - 1440 minutes)
        self.scheduler.add_recurring_task(1440, self._autonomous_research)

        # 3. Reflection (Every 30 minutes)
        # Note: Reflection is also called in the main loop, but we can enforce a dedicated cycle.
        # self.scheduler.add_recurring_task(30, self.run_self_improvement)

    def _autonomous_security_scan(self):
        """
        Task: Scan own codebase for vulnerabilities.
        """
        print("Daemon: Running autonomous security scan...")
        # Simplification: Scan a key file
        try:
            with open("my_son/server.py", "r") as f:
                code = f.read()
            report = self.security.scan_code_vulnerabilities(code)
            # In a real async context we'd await, but scheduler runs in thread.
            # We can't easily await state_manager here without a loop.
            # Just print for now.
            print(f"Security Report: {report[:100]}...")
        except Exception as e:
            print(f"Security Scan Failed: {e}")

    def _autonomous_research(self):
        """
        Task: Research AI advancements and apply SEAL.
        """
        print("Daemon: Running autonomous research...")
        try:
            topic = "Latest advancements in Autonomous AI Agents"
            summary = self.learner.study_topic(topic)
            print(f"Research Summary: {summary[:100]}...")

            # Apply SEAL
            self.seal_engine.perform_adaptation(topic, summary)

        except Exception as e:
            print(f"Research Failed: {e}")

    def run_self_improvement(self):
        """
        Executes the self-improvement pipeline.
        Runs in a separate thread, so must use run_coroutine_threadsafe for async calls.
        """
        # A. Reflection
        plan = self.reflection_module.run_reflection_cycle()
        if not plan:
            return

        # Use run_coroutine_threadsafe to schedule async work on the main loop
        if hasattr(self, 'loop'):
            asyncio.run_coroutine_threadsafe(state_manager.log_activity("Self-Correction Plan generated."), self.loop)

        # B. Code Modification
        if hasattr(self, 'loop'):
            asyncio.run_coroutine_threadsafe(state_manager.update_state("current_task", "Self-Improving"), self.loop)

        patch = self.code_modification_module.generate_patch(plan)
        if not patch:
            return

        # C. Deployment
        if hasattr(self, 'loop'):
            asyncio.run_coroutine_threadsafe(state_manager.log_activity("Deploying patch..."), self.loop)

        success = self.deployment_module.apply_patch(patch)

        if hasattr(self, 'loop'):
            if success:
                asyncio.run_coroutine_threadsafe(state_manager.log_activity("Self-improvement successful."), self.loop)
                # voice_interface.speak is sync or async? It's likely sync using pyttsx3 or similar, but check.
                # If it's safe to run in thread, fine.
                self.voice_interface.speak("I have upgraded my code.")
            else:
                asyncio.run_coroutine_threadsafe(state_manager.log_activity("Deployment failed."), self.loop)

            asyncio.run_coroutine_threadsafe(state_manager.update_state("current_task", "Idle"), self.loop)

if __name__ == "__main__":
    daemon = AutonomousAgentDaemon()
    asyncio.run(daemon.run_loop())

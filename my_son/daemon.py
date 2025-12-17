import asyncio
import time
import os
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

    async def run_loop(self):
        """
        Runs the main loop: Conversation -> Reflection -> Self-Correction.
        """
        print("Starting Autonomous Agent Daemon: My Son is Alive.")
        await state_manager.log_activity("My Son is Alive. Daemon started.")

        # Schedule Default Autonomous Tasks
        self._schedule_default_tasks()

        # Trigger Initial Hacking Skill Acquisition (One-time)
        if not os.path.exists(".hacking_skills_acquired"):
            self.scheduler.add_recurring_task(0, self._acquire_hacking_skills)

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

            # 2. Run Self-Improvement Cycle
            self.run_self_improvement()

            # Sleep briefly to avoid busy loop
            await asyncio.sleep(5)

    def _schedule_default_tasks(self):
        """
        Registers autonomous tasks to the scheduler.
        """
        self.scheduler.add_recurring_task(60, self._autonomous_security_scan)
        self.scheduler.add_recurring_task(1440, self._autonomous_research)

    def _acquire_hacking_skills(self):
        """
        Task: Learn from GitHub 'hacking' topic.
        """
        print("Daemon: Initiating Skill Acquisition: Hacking...")
        try:
            result = self.learner.study_topic("https://github.com/topics/hacking")
            print(result)
            with open(".hacking_skills_acquired", "w") as f:
                f.write("True")
        except Exception as e:
            print(f"Skill Acquisition Failed: {e}")

    def _autonomous_security_scan(self):
        """
        Task: Scan own codebase for vulnerabilities.
        """
        print("Daemon: Running autonomous security scan...")
        try:
            with open("my_son/server.py", "r") as f:
                code = f.read()
            report = self.security.scan_code_vulnerabilities(code)
            print(f"Security Report: {report[:100]}...")
        except Exception as e:
            print(f"Security Scan Failed: {e}")

    def _autonomous_research(self):
        """
        Task: Research AI advancements.
        """
        print("Daemon: Running autonomous research...")
        try:
            summary = self.learner.study_topic("Latest advancements in Autonomous AI Agents")
            print(f"Research Summary: {summary}")
        except Exception as e:
            print(f"Research Failed: {e}")

    def run_self_improvement(self):
        """
        Executes the self-improvement pipeline.
        """
        plan = self.reflection_module.run_reflection_cycle()
        if not plan:
            return

        asyncio.create_task(state_manager.log_activity("Self-Correction Plan generated."))
        asyncio.create_task(state_manager.update_state("current_task", "Self-Improving"))

        patch = self.code_modification_module.generate_patch(plan)
        if not patch:
            return

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

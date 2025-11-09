import sys
import os
import time
import json
import signal
import asyncio
from my_son.daemon import daemonize
from my_son.firebase.firebase_client import FirebaseClient
from my_son.agent.agent import Agent
from my_son.data_analysis.hva import HVAPrioritization
from my_son.action_generation.command import CommandGenerationEngine
from my_son.action_generation.delivery import DeliveryInterface
from my_son.action_generation.tracking import AdherenceTracker
from my_son.action_generation.review import ReviewModule
from my_son.self_improvement.reflection import ReflectionModule
from my_son.meta_efficiency.rac import ResourceAllocationCritic
from my_son.meta_efficiency.rewrite import CodeRewriteFunction
from my_son.system_monitor import SystemMonitor
from my_son.learning.ingestion import KnowledgeIngestionEngine
from my_son.learning.curriculum import CurriculumGenerator
from my_son.learning.mastery import MasteryVerificationProtocol
from my_son.git_integration import GitIntegration
from my_son.self_improvement.deployment import DeploymentModule
from my_son.osint_manager import OSINTServiceManager
from my_son.learning.osint import OSINTClient

# Use absolute paths for all files to avoid issues when daemonized
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PID_FILE = os.path.join(APP_DIR, 'my_son.pid')
LOG_FILE = os.path.join(APP_DIR, 'my_son.log')
CMD_FILE = os.path.join(APP_DIR, 'my_son.cmd')
PERFORMANCE_LOG = os.path.join(APP_DIR, 'performance_logs.jsonl')
INTERNAL_PERFORMANCE_LOG = os.path.join(APP_DIR, 'internal_performance.jsonl')

async def handle_command(command, osint_client):
    """Handles commands from the C2 interface."""
    if command == 'pause':
        return 'pause'
    elif command == 'resume':
        return 'resume'
    elif command == 'reflect':
        print("Forcing a reflection cycle.")
        ReflectionModule(log_file=PERFORMANCE_LOG).run_reflection_cycle()
    elif command == 'snapshot':
        print("Forcing a system snapshot.")
        system_snapshot = SystemMonitor().get_snapshot()
        print(f"System Snapshot: {json.dumps(system_snapshot)}")
    elif command.startswith('learn '):
        topic = command.split(' ', 1)[1]
        print(f"--- Initiating Learning Protocol for '{topic}' ---")
        curriculum_gen = CurriculumGenerator()
        curriculum = curriculum_gen.generate_curriculum(topic)
        print("Generated Curriculum:")
        for step in curriculum:
            print(f"  - {step}")
        ingestion_engine = KnowledgeIngestionEngine(osint_client=osint_client)
        knowledge_base = await ingestion_engine.ingest(topic)
        mastery_protocol = MasteryVerificationProtocol()
        for i, (url, content) in enumerate(knowledge_base.items()):
            if i >= 2:
                break
            print(f"\\n--- Verifying understanding of {url} ---")
            summary = mastery_protocol.summarize_text(content)
            print("Generated Summary:")
            print(summary)
    elif command.startswith('master_language '):
        language = command.split(' ', 1)[1]
        print(f"--- Initiating Language Mastery Protocol for '{language}' ---")
        curriculum_gen = CurriculumGenerator()
        curriculum = curriculum_gen.generate_curriculum(language)
        print("Generated Curriculum:")
        for step in curriculum:
            print(f"  - {step}")
        ingestion_engine = KnowledgeIngestionEngine(osint_client=osint_client)
        knowledge_base = await ingestion_engine.ingest(f"{language} programming language")
        mastery_protocol = MasteryVerificationProtocol()
        for i, (url, content) in enumerate(knowledge_base.items()):
            if i >= 1:
                break
            print(f"\\n--- Verifying understanding of {url} ---")
            summary = mastery_protocol.summarize_text(content)
            print("Generated Summary:")
            print(summary)
        print(f"\\n--- Analyzing practical examples of '{language}' code ---")
        await ingestion_engine.ingest(f"open source {language} projects github")
        print("Identified Key Architectural Patterns (Simulated):")
        print("  - Model-View-Controller (MVC)")
    elif command.startswith('osint '):
        parts = command.split(' ', 2)
        if len(parts) == 3:
            tool, query = parts[1], parts[2]
            print(f"--- Initiating OSINT investigation with '{tool}' on '{query}' ---")
            if tool == 'sherlock':
                results = await osint_client.investigate_username(query)
                print(results)
            elif tool == 'holehe':
                results = await osint_client.check_email(query)
                print(results)
    return None

async def main_loop(osint_process):
    """The main operational loop for the 'My Son' agent."""
    paused = False
    monitor = SystemMonitor()
    osint_client = OSINTClient(osint_process)

    print("Agent initialized and state check passed (simulated).")

    while True:
        if os.path.exists(CMD_FILE):
            with open(CMD_FILE, 'r') as f:
                command = f.read().strip()
            os.remove(CMD_FILE)

            state = await handle_command(command, osint_client)
            if state == 'pause':
                paused = True
            elif state == 'resume':
                paused = False

        if paused:
            await asyncio.sleep(10)
            continue

        print("--- 'My Son' Agent Cycle Starting ---")
        system_snapshot = monitor.get_snapshot()
        print(f"System Snapshot: {json.dumps(system_snapshot)}")

        # Core autonomous loop
        user_tasks = [
            {'name': 'Refactor legacy code', 'goal_alignment': 0.7, 'urgency': 0.5, 'skill_development': 0.8, 'strategic_importance': 0.6},
            {'name': 'Develop new feature X', 'goal_alignment': 0.9, 'urgency': 0.8, 'skill_development': 0.7, 'strategic_importance': 0.9},
        ]
        user_weights = {
            'goal_alignment': 0.4, 'urgency': 0.2,
            'skill_development': 0.1, 'strategic_importance': 0.3
        }
        prioritizer = HVAPrioritization(user_weights)
        ranked_tasks = prioritizer.prioritize_tasks(user_tasks)
        top_hva = ranked_tasks[0]

        command_engine = CommandGenerationEngine()
        command = command_engine.generate_command(top_hva)
        print(f"Autonomous Command Generated: {command}")

        ReflectionModule(log_file=PERFORMANCE_LOG).run_reflection_cycle()
        rac = ResourceAllocationCritic(efficiency_threshold=50)
        inefficient_code = rac.analyze_efficiency()
        authorizations = rac.authorize_rewrite(inefficient_code)
        if authorizations:
            print("Meta-efficiency engine has authorized a code rewrite.")
            target_function = authorizations[0]['target_function']
            target_file = f"my_son/meta_efficiency/{target_function}.py"
            rewriter = CodeRewriteFunction(authorizations[0])
            validated_code = rewriter.rewrite_and_validate(target_file)
            if validated_code:
                deployment_plan = {
                    'target_module': target_file,
                    'refactored_code': validated_code
                }
                DeploymentModule(deployment_plan)._apply_patch()
                git_integration = GitIntegration()
                commit_message = f"Self-Improvement: Optimized '{target_file}'"
                git_integration.commit_changes([target_file], commit_message)

        await asyncio.sleep(60)

async def start_agent():
    """Start the agent daemon and the OSINT server."""
    print("Starting agent...")
    try:
        daemonize(PID_FILE, LOG_FILE)
    except RuntimeError as e:
        print(e)
        sys.exit(1)

    osint_manager = OSINTServiceManager()
    osint_process = await osint_manager.start_server()

    if osint_process:
        await main_loop(osint_process)

def stop_agent():
    """Stop the agent daemon and the OSINT server."""
    if os.path.exists(PID_FILE):
        with open(PID_FILE) as f:
            pid = int(f.read())
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Agent with PID {pid} stopped.")
        except ProcessLookupError:
            pass # Already stopped
    OSINTServiceManager().stop_server()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py [start|stop|status]")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'start':
        asyncio.run(start_agent())
    elif command == 'stop':
        stop_agent()
    elif command == 'status':
        if os.path.exists(PID_FILE):
            with open(PID_FILE) as f:
                pid = f.read().strip()
            print(f"Agent is running with PID: {pid}")
        else:
            print("Agent is not running.")
    else:
        print("Unknown command.")
        sys.exit(1)

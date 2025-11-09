import sys
import os
import time
import json
import signal
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

# Use absolute paths for all files to avoid issues when daemonized
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PID_FILE = os.path.join(APP_DIR, 'my_son.pid')
LOG_FILE = os.path.join(APP_DIR, 'my_son.log')
CMD_FILE = os.path.join(APP_DIR, 'my_son.cmd')
PERFORMANCE_LOG = os.path.join(APP_DIR, 'performance_logs.jsonl')
INTERNAL_PERFORMANCE_LOG = os.path.join(APP_DIR, 'internal_performance.jsonl')

def main_loop():
    """
    The main operational loop for the 'My Son' agent.
    """
    paused = False
    monitor = SystemMonitor()

    # Initialize the agent
    # In a real application, user_id would be dynamically sourced.
    user_id = "test_user"
    # NOTE: The Firebase connection is mocked for this demonstration.
    # In a live environment, 'serviceAccountKey.json' would be required.
    # firebase_client = FirebaseClient('serviceAccountKey.json')
    # agent = Agent(user_id, firebase_client)

    # if not agent.state_check():
    #     print("Halting execution due to failed state check.")
    #     return

    print("Agent initialized and state check passed (simulated).")

    while True:
        # Check for commands from the C2 interface
        if os.path.exists(CMD_FILE):
            with open(CMD_FILE, 'r') as f:
                command = f.read().strip()

            if command == 'pause':
                paused = True
                print("Agent is paused.")
            elif command == 'resume':
                paused = False
                print("Agent is resuming.")
            elif command == 'reflect':
                print("Forcing a reflection cycle.")
                ReflectionModule(log_file=PERFORMANCE_LOG).run_reflection_cycle()
            elif command == 'snapshot':
                print("Forcing a system snapshot.")
                system_snapshot = monitor.get_snapshot()
                print(f"System Snapshot: {json.dumps(system_snapshot)}")
            elif command.startswith('learn '):
                topic = command.split(' ', 1)[1]
                print(f"--- Initiating Learning Protocol for '{topic}' ---")
            elif command.startswith('master_language '):
                language = command.split(' ', 1)[1]
                print(f"--- Initiating Language Mastery Protocol for '{language}' ---")

                # 1. Generate Curriculum
                curriculum_gen = CurriculumGenerator()
                curriculum = curriculum_gen.generate_curriculum(language)
                print("Generated Curriculum:")
                for step in curriculum:
                    print(f"  - {step}")

                # 2. Ingest Knowledge (Theoretical)
                ingestion_engine = KnowledgeIngestionEngine()
                knowledge_base = ingestion_engine.ingest(f"{language} programming language")

                # 3. Verify Mastery (Theoretical)
                mastery_protocol = MasteryVerificationProtocol()
                for i, (url, content) in enumerate(knowledge_base.items()):
                    if i >= 1: # Limit to 1 summary for this demo
                        break
                    print(f"\\n--- Verifying understanding of {url} ---")
                    summary = mastery_protocol.summarize_text(content)
                    print("Generated Summary:")
                    print(summary)

            elif command.startswith('master_language '):
                language = command.split(' ', 1)[1]
                print(f"--- Initiating Language Mastery Protocol for '{language}' ---")

                # 1. Generate Curriculum
                curriculum_gen = CurriculumGenerator()
                curriculum = curriculum_gen.generate_curriculum(language)
                print("Generated Curriculum:")
                for step in curriculum:
                    print(f"  - {step}")

                # 2. Ingest Knowledge (Theoretical)
                ingestion_engine = KnowledgeIngestionEngine()
                knowledge_base = ingestion_engine.ingest(f"{language} programming language")

                # 3. Verify Mastery (Theoretical)
                mastery_protocol = MasteryVerificationProtocol()
                for i, (url, content) in enumerate(knowledge_base.items()):
                    if i >= 1: # Limit to 1 summary for this demo
                        break
                    print(f"\\n--- Verifying understanding of {url} ---")
                    summary = mastery_protocol.summarize_text(content)
                    print("Generated Summary:")
                    print(summary)


                # 4. Ingest Knowledge (Practical - Code Analysis)
                print(f"\\n--- Analyzing practical examples of '{language}' code ---")
                code_examples = ingestion_engine.ingest(f"open source {language} projects github")
                print("Identified Key Architectural Patterns (Simulated):")
                print("  - Model-View-Controller (MVC)")
                print("  - Singleton Pattern")
                print("  - Factory Pattern")

            os.remove(CMD_FILE) # Command has been processed

        if paused:
            time.sleep(10) # Check for resume command every 10 seconds
            continue

        print("--- 'My Son' Agent Cycle Starting ---")

        # 1. System Monitoring
        system_snapshot = monitor.get_snapshot()
        print(f"System Snapshot: {json.dumps(system_snapshot)}")

        # This is the core autonomous loop

        # 1. Analyze Data and Identify HVA
        # (Using mock data for this demonstration)
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

        # 2. Generate and Log Command
        command_engine = CommandGenerationEngine()
        command = command_engine.generate_command(top_hva)
        print(f"Autonomous Command Generated: {command}")

        # 3. Run Self-Improvement and Meta-Efficiency Cycles
        ReflectionModule(log_file=PERFORMANCE_LOG).run_reflection_cycle()
        rac = ResourceAllocationCritic(efficiency_threshold=50)
        inefficient_code = rac.analyze_efficiency()
        authorizations = rac.authorize_rewrite(inefficient_code)
        if authorizations:
            print("Meta-efficiency engine has authorized a code rewrite.")

            # Identify the file to rewrite
            # This is still a simplified approach. A more advanced implementation
            # would use a more sophisticated method to map function names to files.
            target_function = authorizations[0]['target_function']
            target_file = f"my_son/meta_efficiency/{target_function}.py"

            rewriter = CodeRewriteFunction(authorizations[0])
            validated_code = rewriter.rewrite_and_validate(target_file)

            if validated_code:
                deployment_plan = {
                    'target_module': target_file,
                    'refactored_code': validated_code
                }
                # Deploy the changes
                DeploymentModule(deployment_plan)._apply_patch()

                # Commit the self-improvement
                git_integration = GitIntegration()
                commit_message = f"Self-Improvement: Optimized '{target_file}'"
                git_integration.commit_changes([target_file], commit_message)

        print("--- 'My Son' Agent Cycle Complete ---")
        time.sleep(60)

def start_agent():
    """Start the agent daemon."""
    print("Starting agent...")
    try:
        daemonize(PID_FILE, LOG_FILE)
    except RuntimeError as e:
        print(e)
        sys.exit(1)

    main_loop()

def stop_agent():
    """Stop the agent daemon."""
    if not os.path.exists(PID_FILE):
        print("Agent is not running.")
        return

    with open(PID_FILE) as f:
        pid = int(f.read())

    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Agent with PID {pid} stopped.")
    except ProcessLookupError:
        print(f"No process with PID {pid} found.")
        # The PID file is stale. Remove it.
        os.remove(PID_FILE)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py [start|stop|status]")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'start':
        start_agent()
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
        print("Unknown command. Usage: python main.py [start|stop|status]")
        sys.exit(1)

import asyncio
import time
import json
import os
import re
from my_son.agent.agent import Agent
from my_son.agent.llm import LLMClient
from my_son.agent.hive import SubAgentManager
from my_son.agent.tools import ToolExecutor, TOOL_DEFINITIONS
from my_son.sync.migration import MigrationManager
from my_son.config import IS_MASTERMIND, MASTERMIND_IP

class ConversationalEngine:
    """
    The Central Controller: Manages Identity, Logic, Swarm, and Memory.
    """

    def __init__(self, agent: Agent, log_file="performance.jsonl", history_file="chat_history.json"):
        """
        Initializes the conversational engine.
        """
        self.agent = agent
        self.llm = LLMClient()
        self.hive = SubAgentManager()
        self.migration = MigrationManager()
        self.tool_executor = ToolExecutor()
        self.log_file = log_file
        self.history_file = history_file
        self.history = self._load_history()

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_history(self):
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Failed to save history: {e}")

    def _parse_tool_call(self, response):
        """
        Extracts JSON tool call from response.
        """
        try:
            # Look for JSON block
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "{" in response and "}" in response:
                # Try to parse the whole string or substring
                json_str = response.strip()
            else:
                return None

            data = json.loads(json_str)
            if "tool" in data and "args" in data:
                return data
        except:
            return None
        return None

    async def start_conversation(self):
        """
        Placeholder for autonomous conversation initiation or queue checking.
        In API mode, this is mostly passive, but can be used for proactive 'thoughts'.
        """
        # Potentially check for queued messages or internal triggers here.
        # For now, it's a no-op to satisfy the daemon loop.
        pass

    async def handle_user_input(self, user_input: str) -> str:
        """
        Handles a single turn of the conversation.
        Checks identity, executes special commands, and manages the think-act-memorize loop.
        """
        # 1. Identity Check
        # Note: We need to re-import or reload config if it changes at runtime,
        # but for this class, checking the imported var is the standard pattern unless we use a getter.
        # Since config.py uses a global variable updated by update_identity, we should check that.
        from my_son.config import IS_MASTERMIND, MASTERMIND_IP # Re-import to get latest state if modified

        if not IS_MASTERMIND:
            return f"I am a Worker Node. Please connect to the Mastermind at {MASTERMIND_IP or 'unknown IP'}."

        start_time = time.time()
        print(f"ConversationalEngine: Received user input: {user_input}")

        # 2. Trigger Checks (Special Commands)
        lower_input = user_input.lower()

        # A. Soul Transfer
        if "transfer soul" in lower_input:
            # Parse target IP: "transfer soul to 192.168.1.5"
            match = re.search(r"to\s+(\d+\.\d+\.\d+\.\d+)", user_input)
            if match:
                target_ip = match.group(1)
                success = self.migration.transfer_soul(target_ip)
                return "Soul transfer successful. I am now a Worker." if success else "Soul transfer failed."
            else:
                return "Please specify target IP (e.g., 'transfer soul to 192.168.1.5')."

        # B. Hive / Spawn Agent
        if "spawn agent" in lower_input:
            # "spawn agent Coder"
            parts = user_input.split("agent")
            if len(parts) > 1:
                role = parts[1].strip()
                agent_config = self.hive.spawn_agent(role)
                # For now, just confirming creation.
                # Ideally we'd switch context or create a session.
                return f"Spawned agent: {agent_config['name']}. Ready for tasks."

        # 3. Generate Response
        # Update History
        self.history.append({"role": "user", "content": user_input})
        self._save_history()

        # Retrieve Context (RAG)
        context = self.llm.memory.retrieve_context(user_input)

        # Retrieve Contextual Rules (SEAL++)
        rules = self.llm.memory.retrieve_relevant_rules(user_input)

        system_prompt = self.agent.get_prompt()
        if context:
            system_prompt += "\nRELEVANT MEMORIES:\n" + "\n".join([f"- {m}" for m in context])

        if rules:
            system_prompt += f"\nAPPLICABLE LEARNED RULES:\n{rules}\n"

        # Append Tool Definitions
        system_prompt += "\n" + TOOL_DEFINITIONS

        # Build Prompt (System + Recent History)
        # Keep last 20 messages for context window management
        messages = [{"role": "system", "content": system_prompt}] + self.history[-20:]

        # Use Chat API
        response = self.llm.chat_complete(messages)

        # Check for Tool Call
        tool_call = self._parse_tool_call(response)
        if tool_call:
            print(f"ConversationalEngine: Tool Call Detected: {tool_call['tool']}")
            # Execute
            result = self.tool_executor.execute(tool_call['tool'], tool_call['args'])

            # Feed result back
            # We construct a temporary message chain to get final answer
            # We don't necessarily save the tool call JSON to history unless we want to.
            # For user UX, we just want the final answer.
            # But the LLM needs to know it called the tool.

            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "system", "content": f"Tool Output: {result}"})

            final_response = self.llm.chat_complete(messages)
            response = final_response # Override response with final answer

        # Update History with Response
        self.history.append({"role": "assistant", "content": response})
        self._save_history()

        # Save to Long-Term Memory (RAG)
        self.llm.memory.save_context(user_input, response)

        total_duration = time.time() - start_time
        print(f"ConversationalEngine: Generated response.")

        # 4. Log performance
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

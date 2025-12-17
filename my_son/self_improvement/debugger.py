"""
This module provides the Auto-Doctor capabilities for self-healing.
"""
import time
import os
import traceback
import logging
from my_son.agent.llm import LLMClient
from my_son.self_improvement.code_modification import CodeModificationModule
from my_son.self_improvement.deployment import DeploymentModule

class AutoDoctor:
    """
    Monitors for errors and attempts to fix them autonomously.
    """

    def __init__(self, log_file="agent_errors.log"):
        self.logger = logging.getLogger(__name__)
        self.log_file = log_file
        self.llm = LLMClient()
        self.coder = CodeModificationModule()
        self.deployer = DeploymentModule()

        # Ensure log file exists
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write("")

    def monitor_logs(self):
        """
        Continuously monitors the log file for new tracebacks.
        Intended to run in a thread.
        """
        print(f"AutoDoctor: Monitoring {self.log_file}...")
        try:
            with open(self.log_file, "r") as f:
                # Go to the end of the file
                f.seek(0, 2)

                while True:
                    line = f.readline()
                    if not line:
                        time.sleep(1)
                        continue

                    if "Traceback (most recent call last):" in line:
                        print("AutoDoctor: Traceback detected!")
                        # Capture the full traceback
                        tb_lines = [line]
                        while True:
                            next_line = f.readline()
                            if not next_line or (not next_line.startswith(" ") and not next_line.startswith("Traceback")):
                                # End of traceback usually implies a line not indented,
                                # but Python TBs end with the Exception line.
                                # Simple heuristic: Read until we find the Exception line (File ... line ... is intermediate)
                                # Actually, standard TB block is indented after the first line until the Exception type.
                                # We'll just read a block of lines or until a new timestamp/log header appears.
                                # For this simple reader, let's just grab the next 20 lines or until empty.
                                if next_line:
                                    tb_lines.append(next_line)
                                break
                            tb_lines.append(next_line)

                        full_tb = "".join(tb_lines)
                        self.capture_error(full_tb)
        except Exception as e:
            print(f"AutoDoctor Monitor Crashed: {e}")

    def capture_error(self, traceback_str):
        """
        Analyzes the traceback and triggers a fix.
        """
        print("AutoDoctor: Analyzing error...")
        self.auto_fix(traceback_str)

    def auto_fix(self, traceback_str):
        """
        Generates a fix for the given traceback.
        """
        prompt = (
            f"I have encountered a crash. Here is the traceback:\n{traceback_str}\n\n"
            "Analyze the error. Identify the file, line number, and the logic flaw. "
            "Generate a SEARCH/REPLACE patch to fix this bug."
        )

        system_prompt = "You are an expert Python debugger. Fix the code to prevent this error."

        print("AutoDoctor: Consulting LLM for a cure...")
        patch = self.llm.complete(prompt, system_prompt=system_prompt)

        if patch:
            print("AutoDoctor: Applying fix...")
            success = self.deployer.apply_patch(patch)
            if success:
                print("AutoDoctor: Self-healed successfully.")
            else:
                print("AutoDoctor: Failed to apply fix.")
        else:
            print("AutoDoctor: LLM could not generate a patch.")

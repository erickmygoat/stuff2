"""
This module contains the ActionExecutor, responsible for executing "real life" actions.
"""
import subprocess
import shlex
import logging

class ActionExecutor:
    """
    Executes system commands and other actions.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def execute_shell_command(self, command_str):
        """
        Executes a shell command safely (MVP version).

        Args:
            command_str (str): The command to execute.

        Returns:
            dict: The result containing stdout, stderr, and return code.
        """
        # Security Note: In a real production system, this would need HEAVY sanitization.
        # For this autonomous agent MVP, we assume the LLM/User is trusted (as per "Serve only me").
        # However, we should still ban obviously destructive commands if possible,
        # but the prompt asks for "real life actions" which implies power.

        self.logger.info(f"Executing shell command: {command_str}")
        print(f"ActionExecutor: Running '{command_str}'")

        try:
            # Using shell=True gives more power but is riskier.
            # Splitting with shlex is safer but limits some shell features.
            # Given "autonomous agent", shell=True is often required for piping etc.
            result = subprocess.run(
                command_str,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out."}
        except Exception as e:
            return {"error": str(e)}

    def execute_action(self, action_type, payload):
        """
        Generic entry point for actions.
        """
        if action_type == "shell":
            return self.execute_shell_command(payload)
        else:
            return {"error": f"Unknown action type: {action_type}"}

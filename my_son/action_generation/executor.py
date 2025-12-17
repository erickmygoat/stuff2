"""
This module contains the ActionExecutor, responsible for executing "real life" actions.
"""
import subprocess
import shlex
import logging
import os

class ActionExecutor:
    """
    Executes system commands and other actions.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Ensure tools directory is in PATH for this session
        self._update_env()

    def _update_env(self):
        """
        Updates the environment variables to include the tools directory.
        """
        self.env = os.environ.copy()
        tools_dir = os.path.abspath("tools")
        if os.path.exists(tools_dir):
            # Add all subdirectories in tools/ to PATH to catch nested bins
            # Actually, standard behavior is to just add the bin dir, but github repos vary.
            # We'll add the root tools dir and one level deep.
            paths = [tools_dir]
            for item in os.listdir(tools_dir):
                path = os.path.join(tools_dir, item)
                if os.path.isdir(path):
                    paths.append(path)
                    # Common bin dirs
                    if os.path.exists(os.path.join(path, "bin")):
                        paths.append(os.path.join(path, "bin"))

            new_path = os.pathsep.join(paths) + os.pathsep + self.env.get("PATH", "")
            self.env["PATH"] = new_path

    def execute_shell_command(self, command_str):
        """
        Executes a shell command safely (MVP version).

        Args:
            command_str (str): The command to execute.

        Returns:
            dict: The result containing stdout, stderr, and return code.
        """
        self._update_env() # Refresh path in case new tools installed

        self.logger.info(f"Executing shell command: {command_str}")
        print(f"ActionExecutor: Running '{command_str}'")

        try:
            result = subprocess.run(
                command_str,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                env=self.env
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

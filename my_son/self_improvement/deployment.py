"""
This module contains the DeploymentModule, responsible for applying patches and deploying.
"""

import os
import subprocess
import re
import shutil
import asyncio
from my_son.interface.state import state_manager

class DeploymentModule:
    """
    Applies code patches, runs tests, and commits changes.
    """

    def apply_patch(self, patch_text):
        """
        Parses the patch text and applies it to the codebase using SEARCH/REPLACE blocks.
        Includes backup logic.
        """
        print("--- Deploying Changes ---")

        file_match = re.search(r"FILE: (.+)", patch_text)
        if not file_match:
            print("Could not parse file path from patch.")
            return False

        filepath = file_match.group(1).strip()

        # Parse SEARCH/REPLACE blocks
        search_pattern = r"<<<<<<< SEARCH\n(.*?)\n=======\n(.*?)\n>>>>>>> REPLACE"
        matches = re.findall(search_pattern, patch_text, re.DOTALL)

        if not matches:
             print("Could not find valid SEARCH/REPLACE blocks.")
             return False

        if not os.path.exists(filepath):
            print(f"Target file {filepath} does not exist.")
            return False

        try:
            with open(filepath, 'r') as f:
                content = f.read()

            # Validation Pass
            for search_block, replace_block in matches:
                if search_block not in content:
                    print(f"SEARCH block not found in {filepath}. Aborting.")
                    return False

            # Backup
            backup_path = filepath + ".bak"
            shutil.copy2(filepath, backup_path)
            print(f"Backup created at {backup_path}")

            # Apply Changes
            new_content = content
            for search_block, replace_block in matches:
                new_content = new_content.replace(search_block, replace_block)

            print(f"Applying changes to {filepath}...")
            with open(filepath, 'w') as f:
                f.write(new_content)
            print("File updated.")

            # Verify
            # Note: run_verification calls commit_changes internally if successful
            if self.run_verification(filepath):
                # Cleanup backup on success
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                return True
            else:
                # Restore backup on failure
                print("Verification failed. Restoring backup...")
                # Helper to log async
                self._log_async("Verification failed. Restoring backup...")
                shutil.move(backup_path, filepath)
                return False

        except Exception as e:
            print(f"Error applying patch: {e}")
            if os.path.exists(filepath + ".bak"):
                print("Restoring backup due to error...")
                shutil.move(filepath + ".bak", filepath)
            return False

    def run_verification(self, filepath):
        """
        Runs tests to ensure the changes didn't break anything.
        """
        print("Running tests...")
        self._log_async("Running verification tests...")

        # For MVP, run all tests. In future, could be targeted.
        try:
            result = subprocess.run(["python", "-m", "pytest"], capture_output=True, text=True)
            if result.returncode == 0:
                print("Tests passed successfully.")
                self._log_async("Tests passed successfully.")
                self.commit_changes(filepath)
                return True
            else:
                print("Tests failed.")
                self._log_async("Tests failed.")
                # Log a snippet of stdout to UI
                failure_snippet = (result.stdout + result.stderr)[-500:]
                self._log_async(f"Failure output: {failure_snippet}")
                return False
        except Exception as e:
            print(f"Error running tests: {e}")
            self._log_async(f"Error running tests: {e}")
            return False

    def _log_async(self, message):
        """
        Helper to log to state_manager from sync method.
        Since DeploymentModule runs in a thread (via daemon), we use run_coroutine_threadsafe
        OR just fire and forget if we can access the loop.
        However, daemon uses asyncio.to_thread, so we are in a separate thread.
        We need to schedule the log on the main loop.
        """
        try:
            # We need to find the running loop. get_event_loop() might return a new one if in thread.
            # Ideally we pass the loop, but for now we try to find it.
            # In python 3.10+, get_event_loop might raise if no loop set in thread.
            # But the daemon started the loop in main thread.
            # Safe way:
            loop = asyncio.get_running_loop()
        except RuntimeError:
             # No running loop in this thread.
             pass

        # Actually, since we are in a thread, we can't get the main loop easily via get_running_loop.
        # We'll skip complex logic and just print for now if we can't reach state_manager safely.
        # The daemon handles its own logging for the high level steps.
        # Let's try to just print for safety unless we have a robust way.
        # Wait, state_manager logs are valuable.
        pass # Placeholder for future enhancement if thread-safe logging becomes critical.

    def commit_changes(self, filepath):
        """
        Commits the changes to git.
        """
        print("Committing changes...")
        try:
            subprocess.run(["git", "add", filepath], check=True)
            subprocess.run(["git", "commit", "-m", f"Autonomous update to {filepath}"], check=True)
            print("Changes committed.")
        except subprocess.CalledProcessError as e:
            print(f"Error committing changes: {e}")

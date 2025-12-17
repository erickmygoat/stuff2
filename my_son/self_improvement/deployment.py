"""
This module contains the DeploymentModule, responsible for applying patches and deploying.
"""

import os
import subprocess
import re

class DeploymentModule:
    """
    Applies code patches, runs tests, and commits changes.
    """

    def apply_patch(self, patch_text):
        """
        Parses the patch text and applies it to the codebase using SEARCH/REPLACE blocks.
        Format:
        FILE: <path>
        <<<<<<< SEARCH
        <content>
        =======
        <content>
        >>>>>>> REPLACE
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

            for search_block, replace_block in matches:
                # Basic normalization to handle potential whitespace issues from LLM
                if search_block not in content:
                    print(f"SEARCH block not found in {filepath}. Aborting.")
                    # In a real system, we might try fuzzy matching or revert previous changes
                    return False

                content = content.replace(search_block, replace_block)

            print(f"Applying changes to {filepath}...")
            with open(filepath, 'w') as f:
                f.write(content)
            print("File updated.")

        except Exception as e:
            print(f"Error applying patch: {e}")
            return False

        return self.run_verification(filepath)

    def run_verification(self, filepath):
        """
        Runs tests to ensure the changes didn't break anything.
        """
        print("Running tests...")
        # For MVP, run all tests. In future, could be targeted.
        try:
            result = subprocess.run(["python", "-m", "pytest"], capture_output=True, text=True)
            if result.returncode == 0:
                print("Tests passed successfully.")
                self.commit_changes(filepath)
                return True
            else:
                print("Tests failed.")
                print(result.stdout)
                print(result.stderr)
                # Revert changes? For now, just report failure.
                return False
        except Exception as e:
            print(f"Error running tests: {e}")
            return False

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

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
        Parses the patch text and applies it to the codebase.
        Assumes the format:
        FILE: <path>
        CODE:
        <content>
        """
        print("--- Deploying Changes ---")

        # Simple parsing logic for the MVP
        file_match = re.search(r"FILE: (.+)", patch_text)
        if not file_match:
            print("Could not parse file path from patch.")
            return False

        filepath = file_match.group(1).strip()

        # Extract code content (rough extraction)
        # Assumes CODE: is followed by the code until the end or next marker
        # This is a simplification.
        if "CODE:" not in patch_text:
             print("Could not parse code content from patch.")
             return False

        code_content = patch_text.split("CODE:", 1)[1].strip()

        # Remove markdown code fences if present
        if code_content.startswith("```python"):
            code_content = code_content[9:]
        elif code_content.startswith("```"):
            code_content = code_content[3:]

        if code_content.endswith("```"):
            code_content = code_content[:-3]

        code_content = code_content.strip()

        print(f"Applying changes to {filepath}...")
        try:
            # Ensure directory exists
            dirname = os.path.dirname(filepath)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(code_content)
            print("File updated.")
        except Exception as e:
            print(f"Error writing file: {e}")
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

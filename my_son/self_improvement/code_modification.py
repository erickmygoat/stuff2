"""
This module contains the CodeModificationModule, which uses an LLM to generate code patches.
"""
import ast
import re
import os
import logging
from my_son.agent.llm import LLMClient

class CodeModificationModule:
    """
    Takes a Self-Correction Plan and generates a code patch using an LLM.
    Verifies syntax before proposing.
    """

    def __init__(self):
        self.llm = LLMClient()
        self.logger = logging.getLogger(__name__)

    def generate_patch(self, plan_text):
        """
        Generates a code patch based on the provided plan using SEARCH/REPLACE blocks.
        Verifies python syntax.
        """
        print("--- Generating Code Patch ---")

        system_prompt = (
            "You are an expert software engineer. Your task is to write code changes based on a plan. "
            "Do NOT rewrite entire files. Use a SEARCH/REPLACE block format to modify specific sections.\n"
            "Format:\n"
            "FILE: <file_path>\n"
            "<<<<<<< SEARCH\n"
            "<original code to find>\n"
            "=======\n"
            "<new code to replace it with>\n"
            ">>>>>>> REPLACE\n"
            "Ensure the SEARCH block matches the existing code EXACTLY (indentation, whitespace)."
        )

        prompt = (
            f"Based on this Self-Correction Plan:\n{plan_text}\n\n"
            "Please generate the patch."
        )

        patch = self.llm.complete(prompt, system_prompt=system_prompt)
        print(f"Generated Patch:\n{patch}")

        # Validation
        if self._validate_patch_syntax(patch):
            return patch
        else:
            print("CodeModification: Patch validation failed. Rejecting patch.")
            return None

    def _validate_patch_syntax(self, patch_text):
        """
        Parses the patch, applies it in memory, and checks for SyntaxErrors via ast.
        """
        # Parse patch
        file_match = re.search(r"FILE: (.+)", patch_text)
        if not file_match:
            # Maybe it's not a python file or structure is different?
            # If no FILE specified, we can't check syntax easily.
            return True

        filepath = file_match.group(1).strip()

        if not filepath.endswith(".py"):
            return True # Skip validation for non-python files

        if not os.path.exists(filepath):
            # Can't validate if file doesn't exist (unless it's a create op, which isn't handled by this block format)
            return True

        search_pattern = r"<<<<<<< SEARCH\n(.*?)\n=======\n(.*?)\n>>>>>>> REPLACE"
        matches = re.findall(search_pattern, patch_text, re.DOTALL)

        if not matches:
             return True # No blocks found, maybe empty patch?

        try:
            with open(filepath, 'r') as f:
                content = f.read()

            for search_block, replace_block in matches:
                if search_block not in content:
                    print(f"CodeModification: Validation failed. SEARCH block not found in {filepath}.")
                    return False
                content = content.replace(search_block, replace_block)

            # Check Syntax
            ast.parse(content)
            print("CodeModification: Syntax check passed.")
            return True

        except SyntaxError as e:
            print(f"CodeModification: SyntaxError in patched code: {e}")
            return False
        except Exception as e:
            print(f"CodeModification: Validation error: {e}")
            return False

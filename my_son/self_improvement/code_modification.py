"""
This module contains the CodeModificationModule, which uses an LLM to generate code patches.
"""

from my_son.agent.llm import LLMClient

class CodeModificationModule:
    """
    Takes a Self-Correction Plan and generates a code patch using an LLM.
    """

    def __init__(self):
        self.llm = LLMClient()

    def generate_patch(self, plan_text):
        """
        Generates a code patch based on the provided plan using SEARCH/REPLACE blocks.
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
        return patch

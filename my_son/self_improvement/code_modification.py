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
        Generates a code patch based on the provided plan.
        """
        print("--- Generating Code Patch ---")

        system_prompt = (
            "You are an expert software engineer. Your task is to write code changes based on a plan. "
            "Return the changes in a format that describes which file to modify and the new content. "
            "For this MVP, provide the full content of the file that needs modification."
        )

        prompt = (
            f"Based on this Self-Correction Plan:\n{plan_text}\n\n"
            "Please generate the Python code to implement this fix. "
            "Specify the file path and the code block. "
            "Format: \nFILE: <path>\nCODE:\n<code_block>"
        )

        patch = self.llm.complete(prompt, system_prompt=system_prompt)
        print(f"Generated Patch:\n{patch}")
        return patch

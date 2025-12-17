"""
This module provides the Architect persona for advanced coding assistance using RAG.
"""
import os
import logging
from my_son.agent.llm import LLMClient
from my_son.brain.memory import Memory

class Architect:
    """
    Expert Software Architect agent.
    Uses RAG (Retrieval-Augmented Generation) over the codebase to answer complex coding questions.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.llm = LLMClient()
        self.memory = Memory() # Reusing general memory, could separate 'code_memory'

    def index_codebase(self, root_dir="."):
        """
        Scans the codebase and stores file contents in memory for retrieval.
        """
        print(f"Architect: Indexing codebase at {root_dir}...")
        count = 0
        for root, dirs, files in os.walk(root_dir):
            if ".git" in root or "__pycache__" in root or "venv" in root:
                continue

            for file in files:
                if file.endswith((".py", ".html", ".js", ".css", ".md")):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                        # Store in memory with metadata
                        self.memory.store_memory(
                            content,
                            metadata={"source": file_path, "type": "code"}
                        )
                        count += 1
                    except Exception as e:
                        pass
        print(f"Architect: Indexed {count} files.")

    def consult(self, query):
        """
        Answers a coding query using context from the codebase.
        """
        print(f"Architect: Consulting on '{query}'...")

        # Retrieve relevant code
        context = self.memory.retrieve_context(query, n_results=5)

        context_str = ""
        if context:
            context_str = "\nRELEVANT CODE:\n" + "\n".join([f"Snippet:\n{c[:500]}..." for c in context])

        system_prompt = (
            "You are the Lead Architect for this project. "
            "Answer the user's question based on the provided code context. "
            "Be precise, technical, and offer code examples where possible."
        )

        prompt = f"Question: {query}\n{context_str}"

        return self.llm.complete(prompt, system_prompt=system_prompt)

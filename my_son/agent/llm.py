import os
import requests
import json
import logging
from my_son.brain.memory import Memory

class LLMClient:
    """
    A unified client handling Local Sovereignty (Ollama) as default, with fallbacks.
    """

    def __init__(self, api_key=None, model="llama3", api_url="http://localhost:11434/api/generate"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model # Default to local model name
        self.api_url = api_url # Default to Ollama
        self.logger = logging.getLogger(__name__)

        # Initialize Memory
        self.memory = Memory()

        # Mode Selection
        # Default to "local" (Ollama) unless explicitly configured otherwise
        self.mode = "local"
        if self.api_key and "openai.com" in self.api_url:
            self.mode = "remote"

    def complete(self, prompt, system_prompt="You are a helpful assistant.", max_tokens=1000):
        """
        Generates a completion using the local Sovereign Brain.
        """
        # 1. Enhance Prompt with Long-Term Memory
        context = self.memory.retrieve_context(prompt)
        if context:
            memory_block = "\nRELEVANT MEMORIES:\n" + "\n".join([f"- {m}" for m in context]) + "\n"
            system_prompt += memory_block

        # 2. Store the new prompt in memory
        self.memory.save_context(prompt, "") # Store query part

        # 3. Execution
        result = self._complete_local(prompt, system_prompt, max_tokens)

        # 4. Store response
        self.memory.save_context("", result) # Store response part

        return result

    def _complete_local(self, prompt, system_prompt, max_tokens):
        """
        Uses Requests to hit Ollama (Local).
        """
        # Ollama /api/generate format
        data = {
            "model": self.model,
            "prompt": f"{system_prompt}\nUser: {prompt}\nAssistant:",
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.7
            }
        }

        try:
            response = requests.post(self.api_url, json=data, timeout=60)
            response.raise_for_status()
            result = response.json().get('response', '').strip()
            return result
        except Exception as e:
            self.logger.error(f"Local LLM failed: {e}")
            return f"[Error] My brain is offline. Please ensure Ollama is running. ({e})"

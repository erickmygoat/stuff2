import os
import requests
import json
import logging
from my_son.brain.embedded_llm import EmbeddedLLM
from my_son.brain.memory import Memory

class LLMClient:
    """
    A unified client handling Remote APIs, Local Servers (Ollama), and Embedded Inference.
    """

    def __init__(self, api_key=None, model="gpt-4o", api_url="https://api.openai.com/v1/chat/completions"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.api_url = api_url
        self.local_url = "http://localhost:11434/v1/chat/completions" # Default Ollama
        self.logger = logging.getLogger(__name__)

        # Initialize Embedded Components
        self.embedded_brain = EmbeddedLLM()
        self.memory = Memory()

        # Mode Selection
        # If no API key is provided, prefer Embedded, then Local Server.
        self.mode = "remote" if self.api_key else "embedded"

    def complete(self, prompt, system_prompt="You are a helpful assistant.", max_tokens=1000):
        """
        Generates a completion using the best available method.
        """
        # 1. Enhance Prompt with Long-Term Memory (The "Complex Brain")
        context = self.memory.retrieve_context(prompt)
        if context:
            memory_block = "\nRELEVANT MEMORIES:\n" + "\n".join([f"- {m}" for m in context]) + "\n"
            system_prompt += memory_block

        # 2. Store the new prompt in memory (learning from input)
        self.memory.store_memory(f"User Query: {prompt}")

        # 3. Execution
        if self.mode == "embedded":
            return self._complete_embedded(prompt, system_prompt, max_tokens)
        else:
            return self._complete_remote(prompt, system_prompt, max_tokens)

    def _complete_embedded(self, prompt, system_prompt, max_tokens):
        """
        Uses the embedded Llama model.
        """
        response = self.embedded_brain.generate(prompt, system_prompt, max_tokens)

        # Store reasoning/output in memory
        self.memory.store_memory(f"My Response: {response}")

        return response

    def _complete_remote(self, prompt, system_prompt, max_tokens):
        """
        Uses Requests to hit OpenAI or Ollama.
        """
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

        headers = {"Content-Type": "application/json"}
        if self.api_key:
             headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            # Try Remote
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()['choices'][0]['message']['content'].strip()
            self.memory.store_memory(f"My Response: {result}")
            return result
        except Exception as e:
            self.logger.warning(f"Remote LLM failed: {e}. Falling back to Embedded.")
            return self._complete_embedded(prompt, system_prompt, max_tokens)

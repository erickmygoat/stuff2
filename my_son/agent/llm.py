import os
import requests
import json
import logging

class LLMClient:
    """
    A client for interacting with an OpenAI-compatible LLM API,
    with support for local offline fallback.
    """

    def __init__(self, api_key=None, model="gpt-4o", api_url="https://api.openai.com/v1/chat/completions"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.api_url = api_url
        self.local_url = "http://localhost:11434/v1/chat/completions" # Default Ollama port
        self.use_local = False
        self.logger = logging.getLogger(__name__)

        # Check if we should default to local
        if not self.api_key:
             self.use_local = True

    def complete(self, prompt, system_prompt="You are a helpful assistant.", max_tokens=1000):
        """
        Generates a completion for the given prompt.
        """
        # Prepare request data
        data = {
            "model": self.model if not self.use_local else "llama3", # Default local model name
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

        headers = {"Content-Type": "application/json"}
        if self.api_key and not self.use_local:
             headers["Authorization"] = f"Bearer {self.api_key}"

        # Try Primary URL
        try:
            url = self.local_url if self.use_local else self.api_url
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            self.logger.warning(f"Primary LLM call failed: {e}")

            # Fallback logic: If we failed on remote, try local.
            if not self.use_local:
                self.logger.info("Attempting fallback to local LLM...")
                try:
                    data["model"] = "llama3" # Adjust for local
                    response = requests.post(self.local_url, headers=headers, json=data, timeout=30)
                    response.raise_for_status()
                    result = response.json()
                    return result['choices'][0]['message']['content'].strip()
                except Exception as local_e:
                    self.logger.error(f"Local LLM fallback failed: {local_e}")

            # Final fallback: Mock response if everything fails
            return f"[MOCK/OFFLINE RESPONSE] Unable to connect to LLM. Request: {prompt[:50]}..."

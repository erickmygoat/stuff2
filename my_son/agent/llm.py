import os
import requests
import json
import logging

class LLMClient:
    """
    A simple client for interacting with an OpenAI-compatible LLM API.
    """

    def __init__(self, api_key=None, model="gpt-4o", api_url="https://api.openai.com/v1/chat/completions"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.api_url = api_url
        self.logger = logging.getLogger(__name__)

    def complete(self, prompt, system_prompt="You are a helpful assistant.", max_tokens=1000):
        """
        Generates a completion for the given prompt.

        :param prompt: The user prompt.
        :param system_prompt: The system instruction.
        :param max_tokens: Maximum tokens for the response.
        :return: The content of the response message.
        """
        if not self.api_key:
            self.logger.warning("OPENAI_API_KEY is not set. Returning mock response.")
            return f"[MOCK LLM RESPONSE] Processed: {prompt[:50]}..."

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error calling LLM API: {e}")
            return f"Error generating response: {e}"

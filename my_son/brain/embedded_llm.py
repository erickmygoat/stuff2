"""
This module contains the EmbeddedLLM class, which runs the LLM locally using llama.cpp.
"""
import os
import logging
try:
    from llama_cpp import Llama
    LLAMA_AVAILABLE = True
except ImportError:
    LLAMA_AVAILABLE = False

from my_son.brain.model_manager import ModelManager

class EmbeddedLLM:
    """
    A strictly offline, embedded LLM engine.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.model_manager = ModelManager()
        self.llm = None
        self._initialize_model()

    def _initialize_model(self):
        """
        Loads the model into memory.
        """
        if not LLAMA_AVAILABLE:
            self.logger.warning("llama-cpp-python not installed. Embedded brain disabled.")
            return

        model_path = self.model_manager.ensure_model_exists()
        if not model_path:
            self.logger.error("Could not find or download model.")
            return

        print("EmbeddedLLM: Loading model into memory... (This implies a brain-like initialization)")
        try:
            # n_ctx=2048 is decent for conversation.
            # n_threads=None will autoscaling.
            self.llm = Llama(
                model_path=model_path,
                n_ctx=2048,
                verbose=False
            )
            print("EmbeddedLLM: Model loaded successfully.")
        except Exception as e:
            self.logger.error(f"Failed to load Llama model: {e}")

    def generate(self, prompt, system_prompt="You are a helpful assistant.", max_tokens=500):
        """
        Generates text using the embedded model.
        """
        if not self.llm:
             return "[EmbeddedLLM Error] Brain not initialized or libraries missing."

        # Format prompt for Llama 2/3 chat templates (Simulated for TinyLlama/ChatML)
        # TinyLlama uses ChatML usually: <|system|>\n...</s><|user|>\n...</s><|assistant|>

        full_prompt = f"<|system|>\n{system_prompt}</s>\n<|user|>\n{prompt}</s>\n<|assistant|>"

        print("EmbeddedLLM: Thinking...")
        try:
            output = self.llm(
                full_prompt,
                max_tokens=max_tokens,
                stop=["</s>"],
                echo=False,
                temperature=0.7
            )
            return output['choices'][0]['text'].strip()
        except Exception as e:
            self.logger.error(f"Inference error: {e}")
            return f"[EmbeddedLLM Error] Inference failed: {e}"

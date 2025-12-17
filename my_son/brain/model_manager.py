"""
This module manages the downloading and verification of local LLM models.
"""
import os
import logging
from huggingface_hub import hf_hub_download

# Constants for the default model
# Using a small, efficient model for the MVP to ensure it runs on most machines (CPU)
# TinyLlama 1.1B Chat is a good candidate for "fast" and "offline" on generic hardware.
REPO_ID = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
FILENAME = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
MODELS_DIR = "models"

class ModelManager:
    """
    Manages the local AI models.
    """

    def __init__(self, models_dir=MODELS_DIR):
        self.models_dir = models_dir
        self.logger = logging.getLogger(__name__)
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir)

    def ensure_model_exists(self):
        """
        Checks if the model exists locally. If not, downloads it.
        """
        model_path = os.path.join(self.models_dir, FILENAME)

        if os.path.exists(model_path):
            self.logger.info(f"Model found at {model_path}")
            return model_path

        print(f"ModelManager: Model not found. Downloading {FILENAME} from {REPO_ID}...")
        print("This might take a while depending on your internet connection...")

        try:
            # Download the model
            downloaded_path = hf_hub_download(
                repo_id=REPO_ID,
                filename=FILENAME,
                local_dir=self.models_dir,
                local_dir_use_symlinks=False
            )
            print(f"ModelManager: Download complete: {downloaded_path}")
            return downloaded_path
        except Exception as e:
            self.logger.error(f"Failed to download model: {e}")
            print(f"ModelManager: Error downloading model: {e}")
            return None

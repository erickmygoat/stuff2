"""
This module provides Vision capabilities (Image loading and encoding).
"""
import logging
import base64
import io
from PIL import Image

class VisionInterface:
    """
    Handles image processing for the agent's eyes.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def encode_image(self, image_file):
        """
        Encodes an image file (path or file-like) to base64 for LLM consumption.
        """
        try:
            if isinstance(image_file, str):
                with open(image_file, "rb") as f:
                    return base64.b64encode(f.read()).decode('utf-8')
            else:
                # Assume bytes or file-like
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            self.logger.error(f"Vision: Failed to encode image: {e}")
            return None

    def process_image(self, image_data):
        """
        Validates and processes raw image data.
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            # Resize if too large (Ollama/Llava optimization)
            if image.width > 1024 or image.height > 1024:
                image.thumbnail((1024, 1024))

            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            return base64.b64encode(buffered.getvalue()).decode('utf-8')
        except Exception as e:
            self.logger.error(f"Vision: Failed to process image: {e}")
            return None

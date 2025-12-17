"""
This module provides voice capabilities (TTS and STT).
"""
import logging

# Try importing dependencies, handle failure gracefully (e.g. in CI/Sandbox)
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except ImportError:
    STT_AVAILABLE = False

class VoiceInterface:
    """
    Handles Voice-to-Text and Text-to-Voice.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.engine = None
        if TTS_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
            except Exception as e:
                self.logger.warning(f"Failed to init TTS engine: {e}")
                TTS_AVAILABLE = False

    def speak(self, text):
        """
        Converts text to speech.
        """
        print(f"[VOICE OUTPUT]: {text}")
        if TTS_AVAILABLE and self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                self.logger.error(f"TTS Error: {e}")
        else:
            self.logger.info("TTS not available.")

    def listen(self):
        """
        Listens to microphone input and converts to text.
        """
        if not STT_AVAILABLE:
            print("STT not available.")
            return None

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                print(f"[VOICE INPUT]: {text}")
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("Could not understand audio.")
                return None
            except Exception as e:
                self.logger.error(f"STT Error: {e}")
                return None

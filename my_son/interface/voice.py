"""
This module provides voice capabilities (TTS and STT).
Optimized for cross-platform usage (gTTS for Linux/Mac quality, pyttsx3 for Windows native integration).
"""
import logging
import os
import time

# TTS Engines
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# STT Engine
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
        self.os_type = os.name # 'nt' for Windows, 'posix' for Linux/Mac

        # Initialize pyttsx3 engine if on Windows
        self.engine = None
        if self.os_type == 'nt' and PYTTSX3_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
            except Exception as e:
                self.logger.warning(f"Failed to init pyttsx3: {e}")

    def speak(self, text):
        """
        Converts text to speech.
        """
        print(f"[VOICE OUTPUT]: {text}")

        # Strategy: Use pyttsx3 on Windows (Native, Offline, No Popups)
        if self.os_type == 'nt' and self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
                return
            except Exception as e:
                self.logger.error(f"pyttsx3 Error: {e}")

        # Strategy: Use gTTS on Linux/Mac or as fallback
        if GTTS_AVAILABLE:
            try:
                tts = gTTS(text=text, lang='en')
                filename = f"speech_{int(time.time())}.mp3"
                tts.save(filename)

                if self.os_type == 'posix':
                    # Try common linux players
                    os.system(f"mpg123 -q {filename} || aplay {filename} || true")
                elif self.os_type == 'nt':
                    # Fallback for Windows if pyttsx3 failed (not ideal, but audible)
                    os.system(f"start {filename}")

                # Cleanup? Maybe keep cache.
            except Exception as e:
                self.logger.error(f"gTTS Error: {e}")
        else:
            self.logger.warning("No TTS engine available.")

    def listen(self):
        """
        Listens to microphone input and converts to text with ambient noise adjustment.
        """
        if not STT_AVAILABLE:
            print("STT not available.")
            return None

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening... (Adjusting for ambient noise)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
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

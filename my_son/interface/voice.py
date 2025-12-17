"""
This module provides voice capabilities (TTS and STT) using gTTS and SpeechRecognition.
"""
import logging
import os
import time

try:
    from gtts import gTTS
    # We need a way to play audio. os.system with mpg123 or similar is common on linux.
    # For cross-platform, playsound or similar is needed, but for MVP/Sandbox we just simulate or assume standard tools.
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

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

    def speak(self, text):
        """
        Converts text to speech using Google TTS and plays it.
        """
        print(f"[VOICE OUTPUT]: {text}")
        if not GTTS_AVAILABLE:
             self.logger.warning("gTTS not installed.")
             return

        try:
            tts = gTTS(text=text, lang='en')
            filename = f"speech_{int(time.time())}.mp3"
            tts.save(filename)

            # Simple playback logic
            if os.name == 'posix':
                # Try common players
                os.system(f"mpg123 -q {filename} || aplay {filename} || true")
            elif os.name == 'nt':
                os.system(f"start {filename}")

            # Cleanup (optional, maybe keep cache)
            # os.remove(filename)
        except Exception as e:
            self.logger.error(f"TTS Error: {e}")

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
                # Dynamic timeout handled by library somewhat, but we set explicit ones
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

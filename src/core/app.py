"""
HELIX Core Application
"""

from datetime import datetime

from .banner import show_banner
from .logger import log
from .assistant import Assistant

from src.speech.microphone import MicrophoneManager
from src.speech.listener import SpeechListener
from src.speech.voice_manager import VoiceManager


class HelixApp:
    """Main HELIX Application."""

    def __init__(self):

        self.voice = VoiceManager()
        self.microphone = MicrophoneManager()

        # One Whisper engine is shared between
        # wake-word detection and commands.
        self.listener = SpeechListener()

        self.assistant = Assistant()

    def startup(self):

        show_banner()

        log("Initializing HELIX...")
        log("Loading core modules...")
        log("Checking system...")
        log("System Online.")

        print()
        print("Welcome to HELIX!")
        print(
            f"Current Time : "
            f"{datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}"
        )
        print()

        self.microphone.list_microphones()

        return True

    def run(self):

        if not self.startup():
            return

        print("\nHELIX Ready.")

        while True:

            # Wait for wake word.
            self.listener.listen_once()

            self.voice.wake_response()

            while True:

                # Reuse the SAME WhisperListener.
                # It now uses Silero VAD automatically.
                command = self.listener.whisper.listen()

                if not command:
                    continue

                if command in (
                    "bye",
                    "goodbye",
                    "sleep",
                    "go to sleep",
                ):
                    self.voice.speak(
                        "Okay Boss. Going to sleep."
                    )
                    break

                reply, shutdown = self.assistant.handle(command)

                if shutdown:
                    self.voice.shutdown_response()
                    return

                if reply:
                    print(f"\nHELIX: {reply}")
                    self.voice.speak(reply)
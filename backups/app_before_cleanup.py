"""
HELIX Core Application
"""

from datetime import datetime

from .banner import show_banner
from .logger import log
from .command_router import CommandRouter
from .action_executor import ActionExecutor

from speech.microphone import MicrophoneManager
from speech.listener import SpeechListener
from speech.voice_manager import VoiceManager


class HelixApp:
    """Main HELIX Application"""

    def __init__(self):

        self.voice = VoiceManager()

        self.microphone = MicrophoneManager()

        self.listener = SpeechListener()

        self.router = CommandRouter()

        self.executor = ActionExecutor()

    def startup(self):

        show_banner()

        log("Initializing HELIX...")
        log("Loading core modules...")
        log("Checking system...")
        log("System Online.")

        print()
        print("Welcome to HELIX!")
        print(
            f"Current Time : {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}"
        )
        print()

        self.microphone.list_microphones()

    def run(self):

        self.startup()

        print("\nHELIX Core Ready.")

        input("\nPress ENTER to exit...")
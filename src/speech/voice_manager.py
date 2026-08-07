"""
HELIX Voice Manager
"""

from src.speech.voice import VoiceEngine


class VoiceManager:
    """Controls all voice-related features."""

    def __init__(self):
        self.engine = VoiceEngine()

    def speak(self, text: str):
        """Speak any text."""
        self.engine.speak(text)

    def wake_response(self):
        """HELIX wake response."""
        self.speak("Yes Boss. I'm listening.")

    def shutdown_response(self):
        """HELIX shutdown response."""
        self.speak("Goodbye Boss. Have a great day.")
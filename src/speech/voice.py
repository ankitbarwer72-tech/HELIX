"""
HELIX Voice Engine
"""

import pyttsx3


class VoiceEngine:
    """HELIX Text-to-Speech Engine."""

    def __init__(self):

        self.engine = pyttsx3.init()

        self.engine.setProperty(
            "rate",
            170,
        )

        self.engine.setProperty(
            "volume",
            1.0,
        )

    def speak(self, text: str):
        """Speak the given text."""

        self.engine.say(text)
        self.engine.runAndWait()
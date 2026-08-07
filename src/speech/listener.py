
"""
HELIX Whisper Wake Listener
"""

from src.speech.whisper_listener import WhisperListener


class SpeechListener:

    WAKE_WORDS = (
        "hello helix",
        "hey helix",
        "hi helix",
        "helix",
        "sun helix",
        "helix suno",
    )

    def __init__(self):

        print("Loading Whisper Wake Listener...")

        self.whisper = WhisperListener()

        print("Wake Listener Ready.")

    def listen_once(self):

        print("\nWaiting for wake word...\n")

        while True:

            text = self.whisper.listen()

            if not text:
                continue

            for wake in self.WAKE_WORDS:

                if wake in text:

                    print(f"Wake word detected: {wake}")

                    return
"""
HELIX Offline Speech Listener
"""

import json
from pathlib import Path

import sounddevice as sd
from vosk import KaldiRecognizer, Model

from .audio_queue import AudioQueue
from .wake_word import WakeWord


class SpeechListener:

    def __init__(self):

        project_root = Path(__file__).resolve().parents[2]

        model_path = (
            project_root
            / "assets"
            / "models"
            / "vosk-model-small-en-us-0.15"
        )

        print("Loading Vosk model...")

        self.model = Model(str(model_path))

        self.audio = AudioQueue()

        self.sample_rate = 44100

        self.recognizer = KaldiRecognizer(
            self.model,
            self.sample_rate,
        )

        self.wake_word = WakeWord()

        print("Speech Listener Ready.")

    def listen_once(self):

        print("\n🎤 Listening...")

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self.audio.callback,
        ):

            while True:

                data = self.audio.get()

                if self.recognizer.AcceptWaveform(data):

                    result = json.loads(
                        self.recognizer.Result()
                    )

                    text = result.get("text", "").strip().lower()

                    if text:

                        print(f"You Said : {text}")

                        if self.wake_word.detected(text):

                            print("✅ Wake Word Detected!")

                            return text
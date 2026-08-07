"""Offline bilingual command listener."""

import json

import sounddevice as sd
from vosk import KaldiRecognizer

from .audio_queue import AudioQueue


class CommandListener:
    """Uses English and Hindi recognizers in parallel for each voice command."""

    def __init__(self, models, authenticator, sample_rate=44100):

        self.audio = AudioQueue()

        self.sample_rate = sample_rate

        self.authenticator = authenticator

        if not isinstance(models, (list, tuple)):
            models = [models]

        self.recognizers = [
            KaldiRecognizer(model, self.sample_rate)
            for model in models
        ]

        # Speaker model is still attached for future use.
        for recognizer in self.recognizers:
            self.authenticator.configure(recognizer)

    def listen(self):

        print("\nListening for command...")

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self.audio.callback,
        ):

            while True:

                data = self.audio.get()

                candidates = []

                for recognizer in self.recognizers:

                    if recognizer.AcceptWaveform(data):

                        result = json.loads(
                            recognizer.Result()
                        )

                        text = (
                            result.get("text", "")
                            .strip()
                            .lower()
                        )

                        if not text:
                            continue

                        words = result.get("result", [])

                        confidence = (
                            sum(
                                word.get("conf", 0)
                                for word in words
                            )
                            / max(len(words), 1)
                        )

                        candidates.append(
                            (
                                text,
                                confidence,
                            )
                        )

                if candidates:

                    text, _ = max(
                        candidates,
                        key=lambda item: item[1],
                    )

                    print(f"\nCommand : {text}")

                    return text
"""
HELIX Whisper Listener
"""

import os
import tempfile
import time

import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel


class WhisperListener:

    def __init__(self):

        print("Loading Whisper Small Model...")

        self.model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8",
        )

        self.sample_rate = 16000

        print("Whisper Ready.")

    def listen(self):

        print("\n🎤 Listening...")

        duration = 4

        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
        )

        sd.wait()

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        ) as temp_file:

            wav_path = temp_file.name

        write(
            wav_path,
            self.sample_rate,
            audio,
        )

        try:

            segments, info = self.model.transcribe(
                wav_path,
                language="en",
                beam_size=5,
                best_of=5,
                temperature=0,
                vad_filter=True,
                condition_on_previous_text=False,
            )

            text = " ".join(
                s.text.strip()
                for s in segments
            ).lower().strip()

            print(f"\nYou said: {text}")

            return text

        finally:

            if os.path.exists(wav_path):
                os.remove(wav_path)
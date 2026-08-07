"""
HELIX Live Speech Listener
Speech Engine V2
"""

import os
import tempfile

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel


class LiveListener:

    def __init__(self):

        print("Loading Whisper Small...")

        self.model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8",
        )

        self.sample_rate = 16000

        print("Live Listener Ready.")

    def listen(self):

        print("\n🎤 Speak... (HELIX will stop automatically when you stop speaking)")

        recording = []
        silence_frames = 0
        speech_started = False

        silence_threshold = 300
        silence_limit = 20

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
        ) as stream:

            while True:

                data, _ = stream.read(1024)

                recording.append(data.copy())

                volume = np.abs(data).mean()

                if volume > silence_threshold:

                    speech_started = True
                    silence_frames = 0

                elif speech_started:

                    silence_frames += 1

                if speech_started and silence_frames >= silence_limit:
                    break

        audio = np.concatenate(recording, axis=0)

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        ) as temp:

            wav_path = temp.name

        write(
            wav_path,
            self.sample_rate,
            audio,
        )

        try:

            segments, _ = self.model.transcribe(
                wav_path,
                language="en",
                beam_size=5,
                best_of=5,
                vad_filter=True,
                temperature=0,
            )

            text = " ".join(
                segment.text.strip()
                for segment in segments
            ).lower().strip()

            print(f"\nYou said: {text}")

            return text

        finally:

            if os.path.exists(wav_path):
                os.remove(wav_path)
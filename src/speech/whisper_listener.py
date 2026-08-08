"""
HELIX Whisper Listener V2
Silero VAD + Faster-Whisper
"""

import os
import tempfile
from pathlib import Path

import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

from .live_listener import LiveSpeechListener


class WhisperListener:
    """Records speech with Silero VAD and transcribes it with Faster-Whisper."""

    def __init__(self):

        print("Loading Whisper Small Model...")

        self.model_path = (
            Path.home()
            / ".cache"
            / "huggingface"
            / "hub"
            / "models--Systran--faster-whisper-small"
            / "snapshots"
            / "536b0662742c02347bc0e980a01041f333bce120"
        )

        if not self.model_path.is_dir():
            raise FileNotFoundError(
                f"Whisper model not found at: {self.model_path}"
            )

        self.model = WhisperModel(
            str(self.model_path),
            device="cpu",
            compute_type="int8",
        )

        self.sample_rate = 16000

        self.vad_listener = LiveSpeechListener()

        print("Whisper V2 Ready.")

    def listen(self):

        print("\n🎤 Speak your command...")

        audio = self.vad_listener.listen()

        if audio is None or len(audio) == 0:
            print("No speech detected.")
            return ""

        audio = np.asarray(
            audio,
            dtype=np.float32,
        )

        audio = np.clip(
            audio,
            -1.0,
            1.0,
        )

        audio_int16 = (
            audio * 32767
        ).astype(np.int16)

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        ) as temp_file:

            wav_path = temp_file.name

        write(
            wav_path,
            self.sample_rate,
            audio_int16,
        )

        try:

            segments, info = self.model.transcribe(
                wav_path,
                language="en",
                task="transcribe",
                beam_size=7,
                patience=1.0,
                temperature=0,
                condition_on_previous_text=False,
                vad_filter=True,
                without_timestamps=True,
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
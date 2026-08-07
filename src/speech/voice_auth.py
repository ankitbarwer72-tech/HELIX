"""Local owner-voice verification using Vosk speaker embeddings."""

import json
import math
import os
from pathlib import Path

from vosk import SpkModel


class VoiceAuthenticator:
    """Matches Vosk speaker vectors against an enrolled local owner profile."""

    # Lower threshold while we tune voice recognition.
    THRESHOLD = 0.55

    def __init__(self, model_root: Path):

        self.profile_path = (
            Path(
                os.environ.get(
                    "APPDATA",
                    Path.home() / "AppData" / "Roaming",
                )
            )
            / "HELIX"
            / "owner_voice.json"
        )

        speaker_model_path = model_root / "vosk-model-spk-0.4"

        if speaker_model_path.is_dir():
            self.speaker_model = SpkModel(str(speaker_model_path))
        else:
            self.speaker_model = None

        self.owner_vector = self._load_profile()

    @property
    def is_enrolled(self):

        return (
            self.speaker_model is not None
            and bool(self.owner_vector)
        )

    def configure(self, recognizer):

        if self.speaker_model is not None:
            recognizer.SetSpkModel(self.speaker_model)

    def verify(self, result: dict):

        sample = result.get("spk")

        if (
            not self.owner_vector
            or not sample
            or len(sample) != len(self.owner_vector)
        ):
            return False, 0.0

        sample_length = math.sqrt(
            sum(value * value for value in sample)
        )

        if sample_length == 0:
            return False, 0.0

        similarity = sum(
            owner * (value / sample_length)
            for owner, value in zip(
                self.owner_vector,
                sample,
            )
        )

        print(
            f"[Voice Auth] Similarity = {similarity:.3f} | Required = {self.THRESHOLD:.2f}"
        )

        if similarity >= self.THRESHOLD:

            print("[Voice Auth] Owner VERIFIED")

            return True, similarity

        print("[Voice Auth] Owner REJECTED")

        return False, similarity

    def enrol(self, samples: list[list[float]]):

        if len(samples) < 3:
            raise ValueError(
                "Record three voice samples before enrolling."
            )

        size = len(samples[0])

        if (
            not size
            or any(len(sample) != size for sample in samples)
        ):
            raise ValueError(
                "Voice samples were invalid."
            )

        average = [
            sum(sample[index] for sample in samples)
            / len(samples)
            for index in range(size)
        ]

        length = math.sqrt(
            sum(value * value for value in average)
        )

        if length == 0:
            raise ValueError(
                "Voice samples were too quiet."
            )

        self.owner_vector = [
            value / length
            for value in average
        ]

        self.profile_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.profile_path.write_text(
            json.dumps(
                {
                    "version": 1,
                    "threshold": self.THRESHOLD,
                    "vector": self.owner_vector,
                }
            ),
            encoding="utf-8",
        )

    def _load_profile(self):

        try:

            saved = json.loads(
                self.profile_path.read_text(
                    encoding="utf-8"
                )
            )

            vector = saved.get("vector", [])

            if (
                isinstance(vector, list)
                and all(
                    isinstance(value, (int, float))
                    for value in vector
                )
            ):
                return vector

        except (
            OSError,
            ValueError,
            json.JSONDecodeError,
        ):
            pass

        return []
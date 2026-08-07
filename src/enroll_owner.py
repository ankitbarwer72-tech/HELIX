"""Interactive, local-only owner-voice enrollment for HELIX."""

import json
import sys
from pathlib import Path

import sounddevice as sd
from vosk import KaldiRecognizer, Model

from src.speech.audio_queue import AudioQueue
from src.speech.voice_auth import VoiceAuthenticator


def asset_root() -> Path:
    return Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1])) / "assets" / "models"


def record_voice_vector(model, authenticator, sample_rate=44100):
    recognizer = KaldiRecognizer(model, sample_rate)
    authenticator.configure(recognizer)
    audio = AudioQueue()
    with sd.RawInputStream(
        samplerate=sample_rate,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=audio.callback,
    ):
        while True:
            if recognizer.AcceptWaveform(audio.get()):
                result = json.loads(recognizer.Result())
                vector = result.get("spk")
                if vector:
                    return vector


def main():
    models = asset_root()
    authenticator = VoiceAuthenticator(models)
    if authenticator.speaker_model is None:
        raise RuntimeError("Speaker model is missing. Rebuild HELIX before enrolling.")
    model = Model(str(models / "vosk-model-small-en-us-0.15"))
    prompts = (
        "Hello Helix, this laptop belongs to me.",
        "Helix, recognize only my voice.",
        "My personal assistant is ready.",
    )
    print("HELIX Owner Voice Enrollment")
    print("Use a quiet room. Speak each line naturally after pressing Enter.\n")
    samples = []
    for number, prompt in enumerate(prompts, start=1):
        input(f"Sample {number}/3 — press Enter, then say: {prompt}\n")
        print("Listening. Stop speaking and wait one second...")
        samples.append(record_voice_vector(model, authenticator))
        print("Sample saved.\n")
    authenticator.enrol(samples)
    print("Enrollment complete. HELIX will now respond only to your voice.")


if __name__ == "__main__":
    main()

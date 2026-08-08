"""
HELIX Speech Engine V2
Silero VAD based live speech recorder.
"""

import queue
import time

import numpy as np
import sounddevice as sd
import torch
from silero_vad import load_silero_vad


class LiveSpeechListener:
    """Detects speech automatically and returns one complete utterance."""

    def __init__(self):

        print("Loading Silero VAD...")

        self.model = load_silero_vad()

        self.sample_rate = 16000
        self.block_size = 512

        # Use the actual Conexant microphone.
        # This prevents HELIX from accidentally using
        # Stereo Mix or another Windows default input.
        self.input_device = 1

        self.speech_threshold = 0.5
        self.min_speech_duration = 0.25
        self.silence_duration = 0.8
        self.max_recording_duration = 10.0

        device_info = sd.query_devices(self.input_device)

        print(
            f"HELIX Microphone: "
            f"[{self.input_device}] {device_info['name']}"
        )

        print("Silero VAD Ready.")

    def listen(self):
        """
        Listen until speech is detected and then automatically
        stop after the speaker becomes silent.
        """

        audio_queue = queue.Queue()
        speech_chunks = []

        speech_started = False
        speech_start_time = None
        last_speech_time = None

        def callback(indata, frames, time_info, status):

            if status:
                print(status)

            audio_queue.put(indata.copy())

        print("\n🎤 Listening...")

        with sd.InputStream(
            device=self.input_device,
            samplerate=self.sample_rate,
            blocksize=self.block_size,
            channels=1,
            dtype="float32",
            callback=callback,
        ):

            while True:

                audio = audio_queue.get()

                audio_tensor = torch.from_numpy(
                    audio[:, 0]
                )

                speech_probability = self.model(
                    audio_tensor,
                    self.sample_rate,
                ).item()

                current_time = time.monotonic()

                if speech_probability >= self.speech_threshold:

                    if not speech_started:

                        speech_started = True
                        speech_start_time = current_time

                        print("Speech detected...")

                    last_speech_time = current_time

                    speech_chunks.append(audio.copy())

                elif speech_started:

                    speech_chunks.append(audio.copy())

                    silence_time = (
                        current_time - last_speech_time
                    )

                    speech_duration = (
                        current_time - speech_start_time
                    )

                    if (
                        silence_time
                        >= self.silence_duration
                        and speech_duration
                        >= self.min_speech_duration
                    ):
                        break

                    if (
                        speech_duration
                        >= self.max_recording_duration
                    ):
                        break

        if not speech_chunks:
            return None

        audio_data = torch.from_numpy(
            np.concatenate(
                speech_chunks,
                axis=0,
            )[:, 0]
        )

        return audio_data.numpy()
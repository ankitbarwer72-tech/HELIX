"""
HELIX Microphone Manager
"""

import sounddevice as sd


class MicrophoneManager:
    """Handles microphone detection."""

    def list_microphones(self):
        """Print all available input devices."""

        devices = sd.query_devices()

        print("\n========== Available Microphones ==========\n")

        found = False

        for index, device in enumerate(devices):

            if device["max_input_channels"] > 0:

                found = True

                print(f"[{index}] {device['name']}")

        if not found:
            print("No microphone detected.")

        print("\n==========================================\n")
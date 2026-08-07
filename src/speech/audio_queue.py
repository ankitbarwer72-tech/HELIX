"""
HELIX Audio Queue
"""

from queue import Queue


class AudioQueue:
    """Thread-safe queue for microphone audio."""

    def __init__(self):
        self.queue = Queue()

    def callback(self, indata, frames, time, status):
        """Receives audio from the microphone."""

        if status:
            print(status)

        self.queue.put(bytes(indata))

    def get(self):
        """Return next audio chunk."""

        return self.queue.get()
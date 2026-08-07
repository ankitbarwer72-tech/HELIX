"""
HELIX AI Brain
"""

from .provider import AIProvider


class Brain:

    def __init__(self):

        self.ai = AIProvider()

        self.system_prompt = (
            "You are HELIX, a smart desktop AI assistant. "
            "Be concise, helpful and friendly. "
            "Reply in simple English unless the user speaks Hindi or Hinglish. "
            "Keep answers suitable for voice output."
        )

    def think(self, user_message: str) -> str:

        prompt = (
            f"{self.system_prompt}\n\n"
            f"User: {user_message}\n"
            f"HELIX:"
        )

        return self.ai.ask(prompt)
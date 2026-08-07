"""
HELIX Groq AI Provider
"""

from groq import Groq

from .config import (
    GROQ_API_KEY,
    MODEL_NAME,
)


class AIProvider:

    def __init__(self):

        self.client = Groq(
            api_key=GROQ_API_KEY,
        )

        print(f"HELIX AI Ready ({MODEL_NAME})")

    def ask(self, prompt: str) -> str:

        try:

            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            return response.choices[0].message.content

        except Exception as error:

            return f"Groq Error: {error}"
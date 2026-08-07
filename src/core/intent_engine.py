"""
HELIX Intent Engine
Smart speech cleanup and correction.
"""

import re
from rapidfuzz import process, fuzz


class IntentEngine:

    FILLER_WORDS = {
        "please",
        "can",
        "could",
        "would",
        "will",
        "you",
        "hey",
        "helix",
        "boss",
        "for",
        "me",
        "just",
        "kindly",
    }

    REPLACEMENTS = {
        "you tube": "youtube",
        "your tube": "youtube",
        "utube": "youtube",
        "u tube": "youtube",
        "goggle": "google",
        "goo gle": "google",
        "chrome browser": "chrome",
        "start": "open",
        "launch": "open",
        "run": "open",
        "bye bye": "bye",
    }

    KNOWN_WORDS = [
        "youtube",
        "google",
        "chrome",
        "brave",
        "chatgpt",
        "gmail",
        "github",
        "python",
        "demon",
        "slayer",
        "open",
        "search",
        "shutdown",
        "bye",
        "help",
    ]

    def clean(self, text: str) -> str:

        text = (text or "").lower()

        for old, new in self.REPLACEMENTS.items():
            text = text.replace(old, new)

        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        words = []

        for word in text.split():

            if word in self.FILLER_WORDS:
                continue

            match = process.extractOne(
                word,
                self.KNOWN_WORDS,
                scorer=fuzz.ratio,
            )

            if match and match[1] >= 85:
                words.append(match[0])
            else:
                words.append(word)

        cleaned = " ".join(words)

        print(f"Normalized : {cleaned}")

        return cleaned
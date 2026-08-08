"""
HELIX Intent Engine
Smart speech cleanup and English/Hinglish command normalization.
"""

import re

from rapidfuzz import fuzz, process


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
        "me",
        "just",
        "kindly",
    }

    PHRASE_REPLACEMENTS = {
        # Hindi / Hinglish open commands
        "youtube kholo": "open youtube",
        "youtube khol do": "open youtube",
        "youtube khol": "open youtube",

        "google kholo": "open google",
        "google khol do": "open google",
        "google khol": "open google",

        "brave kholo": "open brave",
        "brave khol do": "open brave",
        "brave khol": "open brave",
        "brave chalao": "open brave",
        "brave chala": "open brave",

        "calculator kholo": "open calculator",
        "calculator khol do": "open calculator",
        "calculator khol": "open calculator",
        "calculator chalao": "open calculator",

        "notepad kholo": "open notepad",
        "notepad khol do": "open notepad",
        "notepad khol": "open notepad",

        "settings kholo": "open settings",
        "settings khol do": "open settings",
        "settings khol": "open settings",

        "file explorer kholo": "open file explorer",
        "file explorer khol do": "open file explorer",
        "file explorer khol": "open file explorer",

        # Hindi / Hinglish search commands
        "google par search karo": "search google",
        "google pe search karo": "search google",
        "google par search kar": "search google",
        "google pe search kar": "search google",

        # Speech recognition variations
        "you tube": "youtube",
        "your tube": "youtube",
        "utube": "youtube",
        "u tube": "youtube",
        "goggle": "google",
        "goo gle": "google",
        "chrome browser": "chrome",

        # English command variations
        "start": "open",
        "launch": "open",
        "run": "open",
        "open up": "open",

        # Search variations
        "search on": "search",

        # Shutdown
        "bye bye": "bye",
        "band karo": "shutdown",
        "band kar": "shutdown",
        "shutdown karo": "shutdown",
    }

    WORD_REPLACEMENTS = {
        "kholo": "open",
        "khol": "open",
        "kholna": "open",
        "kholde": "open",
        "chalao": "open",
        "chala": "open",

        "dhundo": "search",
        "dhundho": "search",
        "dhoondo": "search",
        "dhund": "search",

        "karo": "",
        "kar": "",
        "kr": "",
    }

    KNOWN_WORDS = [
        "youtube",
        "google",
        "chrome",
        "brave",
        "chatgpt",
        "gmail",
        "github",
        "reddit",
        "instagram",
        "facebook",
        "linkedin",
        "netflix",
        "amazon",
        "flipkart",
        "wikipedia",

        "open",
        "search",
        "shutdown",
        "bye",
        "help",

        "demon",
        "slayer",
        "python",
        "movie",
        "video",

        "desktop",
        "documents",
        "downloads",
        "pictures",
        "music",
        "videos",
        "settings",
        "calculator",
        "notepad",
        "explorer",
    ]

    def clean(self, text: str) -> str:

        text = (text or "").lower().strip()

        if not text:
            return ""

        text = re.sub(
            r"[^\w\s]",
            " ",
            text,
            flags=re.UNICODE,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        ).strip()

        # Special Hindi/Hinglish Google search structure:
        #
        # google par demon slayer search karo
        # google pe demon slayer search karo
        # google par demon slayer search kar
        #
        # becomes:
        # search google demon slayer
        google_hinglish = re.match(
            r"^google\s+(?:par|pe)\s+(.+?)\s+search(?:\s+(?:karo|kar|kr))?$",
            text,
        )

        if google_hinglish:
            query = google_hinglish.group(1).strip()

            text = f"search google {query}"

        else:

            # Apply phrase replacements first.
            for old, new in sorted(
                self.PHRASE_REPLACEMENTS.items(),
                key=lambda item: len(item[0]),
                reverse=True,
            ):
                text = re.sub(
                    rf"\b{re.escape(old)}\b",
                    new,
                    text,
                )

        text = re.sub(
            r"\s+",
            " ",
            text,
        ).strip()

        words = []

        for word in text.split():

            if word in self.FILLER_WORDS:
                continue

            replacement = self.WORD_REPLACEMENTS.get(
                word,
                word,
            )

            if replacement:
                words.append(replacement)

        text = " ".join(words)

        text = re.sub(
            r"\bopen\s+open\b",
            "open",
            text,
        )

        text = re.sub(
            r"\bsearch\s+search\b",
            "search",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        ).strip()

        final_words = []

        for word in text.split():

            match = process.extractOne(
                word,
                self.KNOWN_WORDS,
                scorer=fuzz.ratio,
            )

            if match and match[1] >= 90:
                final_words.append(match[0])
            else:
                final_words.append(word)

        cleaned = " ".join(final_words)

        print(f"Normalized : {cleaned}")

        return cleaned
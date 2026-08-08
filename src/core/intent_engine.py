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

    HINDI_COMMANDS = {
        "यूट्यूब खोलो": "open youtube",
        "यूट्यूब खोल दो": "open youtube",
        "यूट्यूब खोल": "open youtube",

        "गूगल खोलो": "open google",
        "गूगल खोल दो": "open google",
        "गूगल खोल": "open google",

        "ब्रेव खोलो": "open brave",
        "ब्रेव खोल दो": "open brave",
        "ब्रेव खोल": "open brave",

        "कैलकुलेटर खोलो": "open calculator",
        "कैलकुलेटर खोल दो": "open calculator",
        "कैलकुलेटर खोल": "open calculator",

        "नोटपैड खोलो": "open notepad",
        "नोटपैड खोल दो": "open notepad",
        "नोटपैड खोल": "open notepad",

        "सेटिंग्स खोलो": "open settings",
        "सेटिंग्स खोल दो": "open settings",
        "सेटिंग्स खोल": "open settings",

        "गूगल पर सर्च करो": "search google",
        "गूगल पे सर्च करो": "search google",
        "गूगल पर सर्च कर": "search google",
        "गूगल पे सर्च कर": "search google",

        "बंद करो": "shutdown",
        "बंद कर": "shutdown",
    }

    PHRASE_REPLACEMENTS = {

        # Whisper corrections
        "you tube": "youtube",
        "your tube": "youtube",
        "utube": "youtube",
        "u tube": "youtube",

        "goggle": "google",
        "goo gle": "google",

        "chrome browser": "chrome",

        "demons layer": "demon slayer",
        "demons layers": "demon slayer",
        "demon's layer": "demon slayer",

        # Brave pronunciation variations
        "bareu salaw": "open brave",
        "bareu salao": "open brave",
        "brave salaw": "open brave",
        "brave salao": "open brave",
        "brave salau": "open brave",
        "brave sala": "open brave",

        # Hinglish open commands
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

        # Hinglish search commands
        "google par search karo": "search google",
        "google pe search karo": "search google",
        "google par search kar": "search google",
        "google pe search kar": "search google",

        # English command variations
        "start": "open",
        "launch": "open",
        "run": "open",
        "open up": "open",

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

        "per": "par",

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

        # Exact Hindi commands
        if text in self.HINDI_COMMANDS:

            cleaned = self.HINDI_COMMANDS[text]

            print(f"Normalized : {cleaned}")

            return cleaned

        # Hindi Google search
        google_hindi = re.match(
            r"^गूगल\s+(?:पर|पे)\s+(.+?)\s+सर्च(?:\s+(?:करो|कर))?$",
            text,
        )

        if google_hindi:

            query = google_hindi.group(1).strip()

            cleaned = f"search google {query}"

            print(f"Normalized : {cleaned}")

            return cleaned

        # Preserve Hindi-script text.
        if re.search(r"[\u0900-\u097F]", text):

            print(f"Normalized : {text}")

            return text

        # Remove punctuation.
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

        # Special Hinglish Google search.
        google_hinglish = re.match(
            r"^google\s+(?:par|pe)\s+(.+?)\s+search(?:\s+(?:karo|kar|kr))?$",
            text,
        )

        if google_hinglish:

            query = google_hinglish.group(1).strip()

            text = f"search google {query}"

        else:

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
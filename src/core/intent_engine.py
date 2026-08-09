"""
HELIX Intent Engine V3
Smart English, Hindi and Hinglish command normalization.
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

    # ---------------------------------------------------------
    # Hindi-script exact commands
    # ---------------------------------------------------------

    HINDI_COMMANDS = {
        "\u092f\u0942\u091f\u094d\u092f\u0942\u092c \u0916\u094b\u0932\u094b": "open youtube",
        "\u092f\u0942\u091f\u094d\u092f\u0942\u092c \u0916\u094b\u0932 \u0926\u094b": "open youtube",
        "\u092f\u0942\u091f\u094d\u092f\u0942\u092c \u0916\u094b\u0932": "open youtube",

        "\u0917\u0942\u0917\u0932 \u0916\u094b\u0932\u094b": "open google",
        "\u0917\u0942\u0917\u0932 \u0916\u094b\u0932 \u0926\u094b": "open google",
        "\u0917\u0942\u0917\u0932 \u0916\u094b\u0932": "open google",

        "\u092c\u094d\u0930\u0947\u0935 \u0916\u094b\u0932\u094b": "open brave",
        "\u092c\u094d\u0930\u0947\u0935 \u0916\u094b\u0932 \u0926\u094b": "open brave",
        "\u092c\u094d\u0930\u0947\u0935 \u0916\u094b\u0932": "open brave",

        "\u0915\u0948\u0932\u0915\u0941\u0932\u0947\u091f\u0930 \u0916\u094b\u0932\u094b": "open calculator",
        "\u0915\u0948\u0932\u0915\u0941\u0932\u0947\u091f\u0930 \u0916\u094b\u0932 \u0926\u094b": "open calculator",
        "\u0915\u0948\u0932\u0915\u0941\u0932\u0947\u091f\u0930 \u0916\u094b\u0932": "open calculator",

        "\u0928\u094b\u091f\u092a\u0948\u0921 \u0916\u094b\u0932\u094b": "open notepad",
        "\u0928\u094b\u091f\u092a\u0948\u0921 \u0916\u094b\u0932 \u0926\u094b": "open notepad",
        "\u0928\u094b\u091f\u092a\u0948\u0921 \u0916\u094b\u0932": "open notepad",

        "\u0938\u0947\u091f\u093f\u0902\u0917\u094d\u0938 \u0916\u094b\u0932\u094b": "open settings",
        "\u0938\u0947\u091f\u093f\u0902\u0917\u094d\u0938 \u0916\u094b\u0932 \u0926\u094b": "open settings",
        "\u0938\u0947\u091f\u093f\u0902\u0917\u094d\u0938 \u0916\u094b\u0932": "open settings",

        "\u0917\u0942\u0917\u0932 \u092a\u0930 \u0938\u0930\u094d\u091a \u0915\u0930\u094b": "search google",
        "\u0917\u0942\u0917\u0932 \u092a\u0947 \u0938\u0930\u094d\u091a \u0915\u0930\u094b": "search google",
        "\u0917\u0942\u0917\u0932 \u092a\u0930 \u0938\u0930\u094d\u091a \u0915\u0930": "search google",
        "\u0917\u0942\u0917\u0932 \u092a\u0947 \u0938\u0930\u094d\u091a \u0915\u0930": "search google",

        "\u092c\u0902\u0926 \u0915\u0930\u094b": "shutdown",
        "\u092c\u0902\u0926 \u0915\u0930": "shutdown",
    }

    # ---------------------------------------------------------
    # Direct phrase corrections
    # ---------------------------------------------------------

    PHRASE_REPLACEMENTS = {

        "and mute": "unmute",
        "and muted": "unmute",
        "un mute": "unmute",
        "on mute": "unmute",

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

        # Known Brave speech mistakes
        "bareu salaw": "open brave",
        "bareu salao": "open brave",
        "bareu salau": "open brave",
        "brave salaw": "open brave",
        "brave salao": "open brave",
        "brave salau": "open brave",
        "brave sala": "open brave",

        "brave chalau": "open brave",
        "brave chalao": "open brave",
        "brave chala": "open brave",

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

        # Hinglish Google
        "google par search karo": "search google",
        "google pe search karo": "search google",
        "google par search kar": "search google",
        "google pe search kar": "search google",

        # English
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

    # ---------------------------------------------------------
    # Word-level replacements
    # ---------------------------------------------------------

    WORD_REPLACEMENTS = {
        "kholo": "open",
        "khol": "open",
        "kholna": "open",
        "kholde": "open",

        "chalao": "open",
        "chala": "open",
        "chalau": "open",

        "dhundo": "search",
        "dhundho": "search",
        "dhoondo": "search",
        "dhund": "search",

        "per": "par",

        "karo": "",
        "kar": "",
        "kr": "",
    }

    # ---------------------------------------------------------
    # Known words
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Apps / websites that can be opened
    # ---------------------------------------------------------

    OPEN_TARGETS = {
        "youtube": "youtube",
        "google": "google",
        "brave": "brave",
        "chrome": "chrome",
        "chatgpt": "chatgpt",
        "gmail": "gmail",
        "github": "github",
        "reddit": "reddit",
        "instagram": "instagram",
        "facebook": "facebook",
        "linkedin": "linkedin",
        "netflix": "netflix",
        "amazon": "amazon",
        "flipkart": "flipkart",
        "wikipedia": "wikipedia",
        "calculator": "calculator",
        "notepad": "notepad",
        "settings": "settings",
        "explorer": "explorer",
    }

    # ---------------------------------------------------------
    # Fuzzy app aliases.
    #
    # These are only used when the command has an open-like
    # action, so normal AI questions aren't hijacked.
    # ---------------------------------------------------------

    OPEN_ALIASES = {
        "youtube": [
            "youtube",
            "you tube",
            "utube",
        ],

        "google": [
            "google",
            "goggle",
            "goo gle",
        ],

        "brave": [
            "brave",
            "bareu",
            "bare",
            "prev",
            "braiv",
            "brav",
        ],

        "calculator": [
            "calculator",
            "calc",
            "calculate",
        ],

        "notepad": [
            "notepad",
            "note pad",
        ],

        "settings": [
            "settings",
            "setting",
        ],

        "explorer": [
            "explorer",
            "file explorer",
        ],
    }

    # Words that indicate the user wants to open something.
    OPEN_ACTION_WORDS = {
        "open",
        "launch",
        "start",
        "run",
        "khol",
        "kholo",
        "kholna",
        "kholde",
        "chala",
        "chalao",
        "chalau",
        "chalao",
        "allow",
        "allowed",
    }

    def clean(self, text: str) -> str:

        text = (text or "").lower().strip()

        if not text:
            return ""

        # -------------------------------------------------
        # Exact Hindi commands
        # -------------------------------------------------

        if text in self.HINDI_COMMANDS:

            cleaned = self.HINDI_COMMANDS[text]

            print(f"Normalized : {cleaned}")

            return cleaned

        # -------------------------------------------------
        # Hindi Google search
        # -------------------------------------------------

        google_hindi = re.match(
            r"^गूगल\s+(?:पर|पे)\s+(.+?)\s+सर्च(?:\s+(?:करो|कर))?$",
            text,
        )

        if google_hindi:

            query = google_hindi.group(1).strip()

            cleaned = f"search google {query}"

            print(f"Normalized : {cleaned}")

            return cleaned

        # -------------------------------------------------
        # Preserve Hindi text
        # -------------------------------------------------

        if re.search(r"[\u0900-\u097F]", text):

            print(f"Normalized : {text}")

            return text

        # -------------------------------------------------
        # Punctuation cleanup
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Direct phrase replacements
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Smart fuzzy open-command detection
        #
        # This catches things such as:
        #
        # brave to allow
        # prev chalau
        # bareu salaw
        #
        # without turning:
        #
        # youtube colour
        #
        # into an open command.
        # -------------------------------------------------

        smart_open = self._smart_open_command(text)

        if smart_open:

            print(f"Normalized : {smart_open}")

            return smart_open

        # -------------------------------------------------
        # Special Hinglish Google search
        # -------------------------------------------------

        google_hinglish = re.match(
            r"^google\s+(?:par|pe)\s+(.+?)\s+search(?:\s+(?:karo|kar|kr))?$",
            text,
        )

        if google_hinglish:

            query = google_hinglish.group(1).strip()

            text = f"search google {query}"

        # -------------------------------------------------
        # Word-level cleanup
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Cleanup duplicate command words
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Fuzzy correction of known English words
        # -------------------------------------------------

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

    # ---------------------------------------------------------
    # Smart fuzzy open-command detector
    # ---------------------------------------------------------

    def _smart_open_command(self, text: str):

        words = text.split()

        if len(words) < 2:
            return None

        # -------------------------------------------------
        # First try exact known target.
        # -------------------------------------------------

        first_word = words[0]

        exact_target = None

        if first_word in self.OPEN_TARGETS:

            exact_target = first_word

        # -------------------------------------------------
        # If exact target isn't found, fuzzy-match it.
        #
        # Example:
        # prev -> brave
        # bareu -> brave
        # -------------------------------------------------

        if exact_target is None:

            best_target = None
            best_score = 0

            for target, aliases in self.OPEN_ALIASES.items():

                for alias in aliases:

                    score = fuzz.ratio(
                        first_word,
                        alias,
                    )

                    if score > best_score:

                        best_score = score
                        best_target = target

            # Keep this threshold moderate because Whisper
            # can heavily distort short words.
            if best_score >= 60:

                exact_target = best_target

        if exact_target is None:
            return None

        # -------------------------------------------------
        # Examine remaining words for an open-like action.
        # -------------------------------------------------

        remainder = words[1:]

        action_detected = False

        for word in remainder:

            # Exact action
            if word in self.OPEN_ACTION_WORDS:

                action_detected = True
                break

            # Fuzzy action matching
            best_action_score = 0

            for action_word in (
                "open",
                "kholo",
                "khol",
                "chalao",
                "chalau",
                "chala",
                "allow",
                "salaw",
                "salau",
            ):

                score = fuzz.ratio(
                    word,
                    action_word,
                )

                if score > best_action_score:
                    best_action_score = score

            if best_action_score >= 75:

                action_detected = True
                break

        # -------------------------------------------------
        # Special Whisper pattern:
        #
        # "brave to allow"
        #
        # Whisper may interpret "chalao" this way.
        # -------------------------------------------------

        if (
            exact_target == "brave"
            and "allow" in remainder
        ):

            action_detected = True

        if not action_detected:
            return None

        return f"open {exact_target}"
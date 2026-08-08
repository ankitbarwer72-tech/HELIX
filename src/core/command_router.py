"""
Convert English, Hindi, and Hinglish voice commands into HELIX actions.
"""

import re
from difflib import SequenceMatcher

try:
    from rapidfuzz import fuzz
except ImportError:
    fuzz = None

from .intent_engine import IntentEngine


class CommandRouter:

    FOLDERS = {
        "desktop": "desktop",
        "documents": "documents",
        "document": "documents",
        "downloads": "downloads",
        "download": "downloads",
        "pictures": "pictures",
        "photos": "pictures",
        "music": "music",
        "videos": "videos",
        "video": "videos",
        "home": "home",
        "this pc": "computer",
    }

    APPS = {
        "brave": "brave",
        "browser": "brave",
        "notepad": "notepad",
        "calculator": "calculator",
        "calc": "calculator",
        "settings": "settings",
        "file explorer": "explorer",
        "explorer": "explorer",
    }

    SIMPLE_COMMANDS = {
        "open youtube": "open_youtube",
        "open google": "open_google",
        "open brave": "open_brave",
        "open browser": "open_brave",
        "shutdown": "shutdown",
        "exit": "shutdown",
        "quit": "shutdown",
        "bye": "shutdown",
        "help": "help",
        "what can do": "help",
    }

    def __init__(self):
        self.intent = IntentEngine()

    def route(self, command: str):

        original_command = (command or "").lower().strip()

        if not original_command:
            return "empty", None

        # Handle search commands BEFORE filler-word cleanup.
        # This preserves the word "for" in commands such as:
        # "search google for demon slayer"
        for prefix in (
            "search youtube for ",
            "youtube search for ",
            "youtube search ",
        ):
            if original_command.startswith(prefix):
                query = original_command[len(prefix):].strip()

                if query:
                    return "youtube_search", query

        for prefix in (
            "search google for ",
            "google search for ",
        ):
            if original_command.startswith(prefix):
                query = original_command[len(prefix):].strip()

                if query:
                    return "google_search", query

        # Now perform normal intent cleanup.
        command = self.intent.clean(original_command)

        if not command:
            return "empty", None

        # Search commands after normalization.
        for prefix in (
            "youtube search ",
        ):
            if command.startswith(prefix):
                query = command[len(prefix):].strip()

                if query:
                    return "youtube_search", query

        for prefix in (
            "google search ",
        ):
            if command.startswith(prefix):
                query = command[len(prefix):].strip()

                if query:
                    return "google_search", query

        # Generic "search ..." command.
        if command.startswith("search "):

            query = command[len("search "):].strip()

            # If the user said:
            # "search google demon slayer"
            # treat "google" as the search engine,
            # not as part of the query.
            if query.startswith("google "):
                query = query[len("google "):].strip()

                if query:
                    return "google_search", query

            if query.startswith("youtube "):
                query = query[len("youtube "):].strip()

                if query:
                    return "youtube_search", query

            if query:
                return "google_search", query

        if command == "refresh apps":
            return "refresh_launcher", None

        if command in self.SIMPLE_COMMANDS:
            return self.SIMPLE_COMMANDS[command], None

        target = self._open_request(command)

        if target in self.FOLDERS:
            return "open_folder", self.FOLDERS[target]

        if target in self.APPS:
            return "open_app", self.APPS[target]

        if target:
            return "open_named_item", target

        action, score = self._best_simple_match(command)

        if score >= 85:
            return action, None

        return "unknown", command

    @staticmethod
    def _open_request(command: str):

        match = re.match(
            r"^open (.+)$",
            command,
        )

        if match:
            return match.group(1).strip()

        return None

    def _best_simple_match(self, command: str):

        best_action = None
        best_score = 0

        for phrase, action in self.SIMPLE_COMMANDS.items():

            if fuzz:
                score = fuzz.ratio(command, phrase)
            else:
                score = (
                    SequenceMatcher(
                        None,
                        command,
                        phrase,
                    ).ratio()
                    * 100
                )

            if score > best_score:
                best_score = score
                best_action = action

        return best_action, best_score
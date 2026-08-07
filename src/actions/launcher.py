"""Discover and launch installed Windows apps and commonly used folders locally."""

import os
import re
from pathlib import Path

try:
    from rapidfuzz import fuzz, process
except ImportError:
    fuzz = process = None


class LauncherIndex:
    """In-memory index of Start Menu shortcuts and personal folders.

    The index avoids a slow, privacy-unfriendly crawl of every drive. Windows
    Start Menu is the canonical source for installed apps, while personal
    folders cover the locations a user ordinarily opens by name.
    """

    EXTENSIONS = {".lnk", ".url", ".exe", ".bat", ".cmd"}
    MAX_FOLDER_DEPTH = 3
    MAX_ITEMS = 8_000

    def __init__(self):
        self.items = {}

    def build(self):
        self.items.clear()
        for root in self._app_roots():
            self._scan_apps(root)
        for root in self._folder_roots():
            self._scan_folders(root)
        return len(self.items)

    def find(self, spoken_name: str):
        query = self.normalise(spoken_name)
        if not query:
            return None, None, 0
        if query in self.items:
            return self.items[query], query, 100
        choices = list(self.items)
        if not choices:
            return None, None, 0
        if process:
            match = process.extractOne(query, choices, scorer=fuzz.WRatio)
            if match:
                name, score, _ = match
                return self.items[name], name, score

        from difflib import SequenceMatcher
        name = max(choices, key=lambda value: SequenceMatcher(None, query, value).ratio())
        return self.items[name], name, SequenceMatcher(None, query, name).ratio() * 100

    def _add(self, name: str, path: Path):
        key = self.normalise(name)
        if key and key not in self.items:
            self.items[key] = path

    def _scan_apps(self, root: Path):
        if not root.is_dir():
            return
        try:
            for path in root.rglob("*"):
                if len(self.items) >= self.MAX_ITEMS:
                    return
                if path.is_file() and path.suffix.lower() in self.EXTENSIONS:
                    self._add(path.stem, path)
        except (OSError, PermissionError):
            return

    def _scan_folders(self, root: Path):
        if not root.is_dir():
            return
        try:
            for current, directories, _ in os.walk(root, topdown=True):
                current_path = Path(current)
                depth = len(current_path.relative_to(root).parts)
                if depth > self.MAX_FOLDER_DEPTH:
                    directories[:] = []
                    continue
                for directory in directories:
                    self._add(directory, current_path / directory)
        except (OSError, PermissionError):
            return

    @staticmethod
    def normalise(text: str) -> str:
        text = text.lower().replace("you tube", "youtube")
        return re.sub(r"[^\w\u0900-\u097f]+", " ", text).strip()

    @staticmethod
    def _app_roots():
        program_data = Path(os.environ.get("ProgramData", r"C:\ProgramData"))
        app_data = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        return (
            program_data / "Microsoft" / "Windows" / "Start Menu" / "Programs",
            app_data / "Microsoft" / "Windows" / "Start Menu" / "Programs",
            Path.home() / "Desktop",
        )

    @staticmethod
    def _folder_roots():
        home = Path.home()
        return tuple(home / name for name in ("Desktop", "Documents", "Downloads", "Pictures", "Music", "Videos"))

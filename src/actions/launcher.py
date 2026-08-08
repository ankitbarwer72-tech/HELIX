"""
HELIX Universal Launcher V3

Discovers installed Windows applications, games and folders
while rejecting broken/dead shortcuts and unsafe fuzzy matches.
"""

import os
import re
import winreg
from pathlib import Path


class LauncherIndex:

    EXTENSIONS = {
        ".lnk",
        ".url",
        ".exe",
        ".bat",
        ".cmd",
    }

    MAX_FOLDER_DEPTH = 3
    MAX_ITEMS = 12000

    REGISTRY_PATHS = (
        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        ),
        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
        ),
        (
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        ),
    )

    def __init__(self):
        self.items = {}

    # =========================================================
    # BUILD INDEX
    # =========================================================

    def build(self):

        self.items.clear()

        # Start Menu + Desktop
        for root in self._app_roots():
            self._scan_apps(root)

        # Personal folders
        for root in self._folder_roots():
            self._scan_folders(root)

        # Registry-installed applications
        self._scan_registry_apps()

        return len(self.items)

    # =========================================================
    # FIND
    # =========================================================

    def find(self, spoken_name: str):

        query = self.normalise(spoken_name)

        if not query:
            return None, None, 0

        # Exact match
        if query in self.items:

            return (
                self.items[query],
                query,
                100,
            )

        choices = list(self.items)

        if not choices:
            return None, None, 0

        # -----------------------------------------------------
        # Fuzzy matching
        # -----------------------------------------------------

        try:

            from rapidfuzz import fuzz, process

            match = process.extractOne(
                query,
                choices,
                scorer=fuzz.WRatio,
            )

            if match:

                name, score, _ = match

                # Never return a very weak match.
                if score < 72:
                    return None, None, score

                return (
                    self.items[name],
                    name,
                    score,
                )

        except ImportError:
            pass

        # -----------------------------------------------------
        # Standard library fallback
        # -----------------------------------------------------

        from difflib import SequenceMatcher

        best_name = None
        best_score = 0

        for name in choices:

            score = (
                SequenceMatcher(
                    None,
                    query,
                    name,
                ).ratio()
                * 100
            )

            if score > best_score:

                best_score = score
                best_name = name

        if best_name is None or best_score < 72:

            return None, None, best_score

        return (
            self.items[best_name],
            best_name,
            best_score,
        )

    # =========================================================
    # ADD ITEM
    # =========================================================

    def _add(self, name: str, path: Path):

        key = self.normalise(name)

        if not key:
            return

        if key in self.items:
            return

        if len(self.items) >= self.MAX_ITEMS:
            return

        try:

            path = Path(path)

        except (
            OSError,
            TypeError,
        ):

            return

        # -----------------------------------------------------
        # Validate launch target
        # -----------------------------------------------------

        if not self._is_valid_target(path):

            return

        self.items[key] = path

    # =========================================================
    # TARGET VALIDATION
    # =========================================================

    @staticmethod
    def _is_valid_target(path: Path):

        try:

            if not path.exists():
                return False

        except OSError:

            return False

        suffix = path.suffix.lower()

        # Normal executable / batch / command files
        if suffix in {
            ".exe",
            ".bat",
            ".cmd",
        }:

            return path.is_file()

        # LNK must physically exist.
        if suffix == ".lnk":

            return path.is_file()

        # -----------------------------------------------------
        # URL shortcuts
        # -----------------------------------------------------

        if suffix == ".url":

            return LauncherIndex._valid_url_shortcut(path)

        return False

    # =========================================================
    # URL SHORTCUT VALIDATION
    # =========================================================

    @staticmethod
    def _valid_url_shortcut(path: Path):

        try:

            content = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        except (
            OSError,
            UnicodeError,
        ):

            return False

        match = re.search(
            r"^URL=(.+)$",
            content,
            flags=re.IGNORECASE | re.MULTILINE,
        )

        if not match:

            return False

        url = match.group(1).strip()

        # -----------------------------------------------------
        # Normal web URL
        # -----------------------------------------------------

        if url.startswith(
            (
                "http://",
                "https://",
            )
        ):

            return True

        # -----------------------------------------------------
        # Steam shortcut
        # -----------------------------------------------------

        if url.lower().startswith(
            "steam://"
        ):

            return LauncherIndex._steam_available()

        # -----------------------------------------------------
        # Other registered URI schemes
        #
        # These are allowed because Windows may handle them.
        # -----------------------------------------------------

        if re.match(
            r"^[a-zA-Z][a-zA-Z0-9+.-]*://",
            url,
        ):

            return True

        return False

    # =========================================================
    # STEAM CHECK
    # =========================================================

    @staticmethod
    def _steam_available():

        possible_paths = (
            Path(
                r"C:\Program Files (x86)\Steam\steam.exe"
            ),
            Path(
                r"C:\Program Files\Steam\steam.exe"
            ),
            Path.home()
            / "AppData"
            / "Local"
            / "Steam"
            / "Steam.exe",
        )

        for path in possible_paths:

            try:

                if path.is_file():

                    return True

            except OSError:

                continue

        return False

    # =========================================================
    # START MENU / DESKTOP SCAN
    # =========================================================

    def _scan_apps(self, root: Path):

        if not root.is_dir():
            return

        try:

            for path in root.rglob("*"):

                if len(self.items) >= self.MAX_ITEMS:
                    return

                if not path.is_file():
                    continue

                if path.suffix.lower() not in self.EXTENSIONS:
                    continue

                self._add(
                    path.stem,
                    path,
                )

        except (
            OSError,
            PermissionError,
        ):

            return

    # =========================================================
    # FOLDER SCAN
    # =========================================================

    def _scan_folders(self, root: Path):

        if not root.is_dir():
            return

        try:

            for current, directories, _ in os.walk(
                root,
                topdown=True,
            ):

                current_path = Path(current)

                depth = len(
                    current_path.relative_to(root).parts
                )

                if depth > self.MAX_FOLDER_DEPTH:

                    directories[:] = []

                    continue

                for directory in directories:

                    self._add(
                        directory,
                        current_path / directory,
                    )

        except (
            OSError,
            PermissionError,
        ):

            return

    # =========================================================
    # REGISTRY APPLICATION DISCOVERY
    # =========================================================

    def _scan_registry_apps(self):

        for hive, subkey in self.REGISTRY_PATHS:

            try:

                with winreg.OpenKey(
                    hive,
                    subkey,
                ) as root:

                    count = winreg.QueryInfoKey(root)[0]

                    for index in range(count):

                        try:

                            app_key_name = winreg.EnumKey(
                                root,
                                index,
                            )

                            with winreg.OpenKey(
                                root,
                                app_key_name,
                            ) as key:

                                display_name = self._value(
                                    key,
                                    "DisplayName",
                                )

                                if not display_name:
                                    continue

                                display_icon = self._value(
                                    key,
                                    "DisplayIcon",
                                )

                                install_location = self._value(
                                    key,
                                    "InstallLocation",
                                )

                                target = (
                                    self._resolve_registry_target(
                                        display_icon,
                                        install_location,
                                    )
                                )

                                if target:

                                    self._add(
                                        display_name,
                                        target,
                                    )

                        except (
                            OSError,
                            PermissionError,
                        ):

                            continue

            except (
                OSError,
                PermissionError,
            ):

                continue

    # =========================================================
    # REGISTRY VALUE
    # =========================================================

    @staticmethod
    def _value(key, name):

        try:

            return winreg.QueryValueEx(
                key,
                name,
            )[0]

        except (
            OSError,
            TypeError,
        ):

            return None

    # =========================================================
    # REGISTRY TARGET
    # =========================================================

    @staticmethod
    def _resolve_registry_target(
        display_icon,
        install_location,
    ):

        # -----------------------------------------------------
        # DisplayIcon
        # -----------------------------------------------------

        if display_icon:

            value = str(
                display_icon
            ).strip()

            value = value.strip('"')

            value = re.split(
                r",\s*-?\d+\s*$",
                value,
            )[0]

            value = value.strip().strip('"')

            value = os.path.expandvars(
                value,
            )

            try:

                path = Path(value)

                if (
                    path.is_file()
                    and path.suffix.lower() == ".exe"
                ):

                    return path

            except (
                OSError,
                ValueError,
            ):

                pass

        # -----------------------------------------------------
        # InstallLocation
        # -----------------------------------------------------

        if install_location:

            try:

                folder = Path(
                    os.path.expandvars(
                        str(
                            install_location
                        )
                        .strip()
                        .strip('"'),
                    )
                )

            except (
                OSError,
                ValueError,
            ):

                return None

            if folder.is_file():

                return folder

            if not folder.is_dir():

                return None

            try:

                candidates = [
                    path
                    for path in folder.rglob("*.exe")
                    if path.is_file()
                ]

            except (
                OSError,
                PermissionError,
            ):

                return None

            if not candidates:

                return None

            preferred_names = {
                "launch",
                "launcher",
                "app",
                "client",
                "game",
            }

            candidates.sort(
                key=lambda path: (
                    0
                    if path.stem.lower()
                    in preferred_names
                    else 1,
                    len(path.parts),
                    len(path.name),
                )
            )

            return candidates[0]

        return None

    # =========================================================
    # NORMALIZATION
    # =========================================================

    @staticmethod
    def normalise(text: str) -> str:

        text = (
            text
            .lower()
            .replace(
                "you tube",
                "youtube",
            )
        )

        return re.sub(
            r"[^\w\u0900-\u097f]+",
            " ",
            text,
        ).strip()

    # =========================================================
    # APP ROOTS
    # =========================================================

    @staticmethod
    def _app_roots():

        program_data = Path(
            os.environ.get(
                "ProgramData",
                r"C:\ProgramData",
            )
        )

        app_data = Path(
            os.environ.get(
                "APPDATA",
                Path.home()
                / "AppData"
                / "Roaming",
            )
        )

        return (
            program_data
            / "Microsoft"
            / "Windows"
            / "Start Menu"
            / "Programs",

            app_data
            / "Microsoft"
            / "Windows"
            / "Start Menu"
            / "Programs",

            Path.home()
            / "Desktop",
        )

    # =========================================================
    # PERSONAL FOLDER ROOTS
    # =========================================================

    @staticmethod
    def _folder_roots():

        home = Path.home()

        return tuple(
            home / name
            for name in (
                "Desktop",
                "Documents",
                "Downloads",
                "Pictures",
                "Music",
                "Videos",
            )
        )
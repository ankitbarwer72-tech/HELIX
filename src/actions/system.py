"""
Local Windows actions.
No shell commands are constructed from voice input.
"""

import ctypes
import os
import subprocess
from pathlib import Path

from src.actions.launcher import LauncherIndex


class SystemActions:

    FOLDERS = {
        "desktop": Path.home() / "Desktop",
        "documents": Path.home() / "Documents",
        "downloads": Path.home() / "Downloads",
        "pictures": Path.home() / "Pictures",
        "music": Path.home() / "Music",
        "videos": Path.home() / "Videos",
        "home": Path.home(),
        "computer": "shell:MyComputerFolder",
    }

    APPS = {
        "notepad": ["notepad.exe"],
        "calculator": ["calc.exe"],
        "settings": [
            "cmd",
            "/c",
            "start",
            "",
            "ms-settings:",
        ],
        "explorer": ["explorer.exe"],
    }

    # Windows multimedia keys
    VK_VOLUME_MUTE = 0xAD
    VK_VOLUME_DOWN = 0xAE
    VK_VOLUME_UP = 0xAF

    KEYEVENTF_KEYUP = 0x0002

    def __init__(self):

        self.launcher = LauncherIndex()

        item_count = self.launcher.build()

        print(
            f"HELIX launcher ready: "
            f"{item_count} apps and folders indexed."
        )

    def refresh_launcher(self):

        count = self.launcher.build()

        print(
            f"HELIX launcher refreshed: "
            f"{count} apps and folders indexed."
        )

        return count

    # ---------------------------------------------------------
    # Volume controls
    # ---------------------------------------------------------

    @staticmethod
    def _press_media_key(key_code: int):

        ctypes.windll.user32.keybd_event(
            key_code,
            0,
            0,
            0,
        )

        ctypes.windll.user32.keybd_event(
            key_code,
            0,
            SystemActions.KEYEVENTF_KEYUP,
            0,
        )

    def volume_up(self) -> bool:

        try:

            self._press_media_key(
                self.VK_VOLUME_UP
            )

            print("Volume increased.")

            return True

        except Exception as error:

            print(
                f"Could not increase volume: {error}"
            )

            return False

    def volume_down(self) -> bool:

        try:

            self._press_media_key(
                self.VK_VOLUME_DOWN
            )

            print("Volume decreased.")

            return True

        except Exception as error:

            print(
                f"Could not decrease volume: {error}"
            )

            return False

    def toggle_mute(self) -> bool:

        try:

            self._press_media_key(
                self.VK_VOLUME_MUTE
            )

            print("Mute toggled.")

            return True

        except Exception as error:

            print(
                f"Could not toggle mute: {error}"
            )

            return False

    # ---------------------------------------------------------
    # App / launcher controls
    # ---------------------------------------------------------

    def open_named_item(self, name: str):
        """
        Open an indexed Start Menu shortcut,
        executable, URL shortcut, or discovered item.

        If the item is not currently found, refresh the
        launcher once and try again.
        """

        target, match, score = self.launcher.find(name)

        if target is None or score < 72:

            print(
                f"'{name}' was not found in the current "
                "launcher index. Refreshing..."
            )

            self.refresh_launcher()

            target, match, score = self.launcher.find(name)

        if target is None or score < 72:

            print(
                f"I could not find an app or folder named: "
                f"{name}"
            )

            return False, None

        try:

            os.startfile(str(target))

            print(
                f"Opened {match} "
                f"({score:.0f}% match)."
            )

            return True, match

        except OSError as error:

            print(
                f"Could not open {match}: {error}"
            )

            return False, match

    def open_folder(self, name: str) -> bool:

        target = self.FOLDERS.get(name)

        if target is None:

            print(
                "That folder is not configured."
            )

            return False

        try:

            if isinstance(target, Path):

                target.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                os.startfile(str(target))

            else:

                subprocess.Popen(
                    [
                        "explorer.exe",
                        target,
                    ]
                )

            print(
                f"Opened {name}."
            )

            return True

        except OSError as error:

            print(
                f"Could not open {name}: {error}"
            )

            return False

    def open_app(self, name: str) -> bool:

        if name == "brave":

            from src.actions.browser import BrowserActions

            return BrowserActions().open_brave()

        command = self.APPS.get(name)

        if not command:

            print(
                "That app is not configured."
            )

            return False

        try:

            subprocess.Popen(command)

            print(
                f"Opened {name}."
            )

            return True

        except OSError as error:

            print(
                f"Could not open {name}: {error}"
            )

            return False
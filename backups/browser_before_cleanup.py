"""
HELIX Browser Actions
"""

import subprocess
from pathlib import Path
from urllib.parse import quote_plus


class BrowserActions:
    """Browser related actions."""

    def __init__(self):
        self.brave_path = self.find_brave()

    def find_brave(self):

        possible_paths = [
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
            str(
                Path.home()
                / "AppData"
                / "Local"
                / "BraveSoftware"
                / "Brave-Browser"
                / "Application"
                / "brave.exe"
            ),
        ]

        for path in possible_paths:
            if Path(path).exists():
                return path

        return None

    def open_url(self, url):

        if self.brave_path is None:
            print("Brave Browser not found.")
            return False

        try:
            subprocess.Popen([self.brave_path, url])
            return True

        except Exception as e:
            print(f"Error: {e}")
            return False

    def open_chrome(self):

        if self.open_url("https://www.google.com"):
            print("Brave Browser opened.")

    def open_google(self):

        if self.open_url("https://www.google.com"):
            print("Google opened in Brave.")

    def open_youtube(self):

        if self.open_url("https://www.youtube.com"):
            print("YouTube opened in Brave.")

    def google_search(self, query):

        url = (
            "https://www.google.com/search?q="
            + quote_plus(query)
        )

        if self.open_url(url):
            print(f"Searching: {query}")
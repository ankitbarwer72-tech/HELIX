"""
HELIX Browser Actions
"""

import subprocess
from pathlib import Path
from urllib.parse import quote_plus


class BrowserActions:

    WEBSITES = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "chatgpt": "https://chatgpt.com",
        "gmail": "https://mail.google.com",
        "github": "https://github.com",
        "reddit": "https://www.reddit.com",
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "linkedin": "https://www.linkedin.com",
        "netflix": "https://www.netflix.com",
        "prime video": "https://www.primevideo.com",
        "amazon": "https://www.amazon.in",
        "flipkart": "https://www.flipkart.com",
        "wikipedia": "https://wikipedia.org",
        "x": "https://x.com",
        "twitter": "https://x.com",
    }

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

    def _open_url(self, url):

        if self.brave_path is None:
            print("Brave Browser not found.")
            return False

        try:
            subprocess.Popen([self.brave_path, url])
            return True
        except Exception as error:
            print(error)
            return False

    def open_google(self):
        return self.open_website("google")

    def open_youtube(self):
        return self.open_website("youtube")

    def open_brave(self):

        if self.brave_path is None:
            print("Brave Browser not found.")
            return False

        subprocess.Popen([self.brave_path])
        return True

    def open_chrome(self):
        return self.open_brave()

    def open_website(self, name):

        url = self.WEBSITES.get(name.lower())

        if not url:
            print(f"Unknown website: {name}")
            return False

        return self._open_url(url)

    def google_search(self, query):

        if not query:
            return

        url = (
            "https://www.google.com/search?q="
            + quote_plus(query)
        )

        self._open_url(url)

    def youtube_search(self, query):

        if not query:
            return

        url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(query)
        )

        self._open_url(url)
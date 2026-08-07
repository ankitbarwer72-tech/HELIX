"""
HELIX Action Executor
"""

from actions.browser import BrowserActions


class ActionExecutor:
    """Executes actions returned by CommandRouter."""

    def __init__(self):
        self.browser = BrowserActions()

    def execute(self, action, data=None):

        if action == "open_chrome":
            self.browser.open_chrome()
            return None

        elif action == "open_google":
            self.browser.open_google()
            return None

        elif action == "open_youtube":
            self.browser.open_youtube()
            return None

        elif action == "google_search":
            self.browser.google_search(data)
            return None

        elif action == "shutdown":
            print("Goodbye Boss.")
            return "shutdown"

        elif action == "unknown":
            print(f"I don't understand: {data}")
            return None

        return None
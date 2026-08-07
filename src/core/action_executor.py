"""
Execute the safe actions understood by HELIX.
"""

from src.actions.browser import BrowserActions
from src.actions.system import SystemActions


class ActionExecutor:

    def __init__(self):
        self.browser = BrowserActions()
        self.system = SystemActions()

    def execute(self, action, data=None):

        # ---------- Websites ----------

        if action == "open_google":
            self.browser.open_website("google")
            return "Opening Google."

        elif action == "open_youtube":
            self.browser.open_website("youtube")
            return "Opening YouTube."

        elif action == "open_chatgpt":
            self.browser.open_website("chatgpt")
            return "Opening ChatGPT."

        elif action == "open_gmail":
            self.browser.open_website("gmail")
            return "Opening Gmail."

        elif action == "open_github":
            self.browser.open_website("github")
            return "Opening GitHub."

        elif action == "open_instagram":
            self.browser.open_website("instagram")
            return "Opening Instagram."

        elif action == "open_facebook":
            self.browser.open_website("facebook")
            return "Opening Facebook."

        elif action == "open_linkedin":
            self.browser.open_website("linkedin")
            return "Opening LinkedIn."

        elif action == "open_reddit":
            self.browser.open_website("reddit")
            return "Opening Reddit."

        elif action == "open_netflix":
            self.browser.open_website("netflix")
            return "Opening Netflix."

        elif action == "open_amazon":
            self.browser.open_website("amazon")
            return "Opening Amazon."

        elif action == "open_flipkart":
            self.browser.open_website("flipkart")
            return "Opening Flipkart."

        elif action == "open_wikipedia":
            self.browser.open_website("wikipedia")
            return "Opening Wikipedia."

        elif action == "open_x":
            self.browser.open_website("x")
            return "Opening X."

        # ---------- Browser ----------

        elif action == "open_brave":
            self.browser.open_brave()
            return "Opening Brave."

        elif action == "google_search":
            self.browser.google_search(data)
            return f"Searching Google for {data}."

        elif action == "youtube_search":
            self.browser.youtube_search(data)
            return f"Searching YouTube for {data}."

        # ---------- System ----------

        elif action == "open_folder":
            self.system.open_folder(data)
            return f"Opening {data}."

        elif action == "open_app":
            self.system.open_app(data)
            return f"Opening {data}."

        elif action == "open_named_item":
            opened, resolved = self.system.open_named_item(data)

            if opened:
                return f"Opening {resolved}."

            return f"I could not find {data}. Say refresh apps."

        elif action == "refresh_launcher":
            count = self.system.refresh_launcher()
            return f"Launcher refreshed. Found {count} apps."

        elif action == "help":

            message = (
                "You can ask me to open apps, folders, websites "
                "or search Google and YouTube."
            )

            print(message)

            return message

        elif action == "shutdown":
            print("Goodbye Boss.")
            return "shutdown"

        print(f"Unknown action: {action}")
        return None
"""Wake-word aliases in English and Hindi."""


class WakeWord:
    def __init__(self):
        self.aliases = [
            "hello helix", "hey helix", "hi helix", "sun helix", "helix",
            "hello alex", "hey alex", "hi alex", "alex",
            "hello her legs", "hello her leaks", "hello her looks",
            "hey her legs", "hey her leaks", "hi her legs", "hi her leaks",
            "हेलिक्स", "हेलो हेलिक्स", "हे हेलिक्स", "हाय हेलिक्स",
        ]

    def detected(self, text: str) -> bool:
        text = (text or "").lower().strip()
        return any(wake in text for wake in self.aliases)

"""
HELIX Assistant

Handles both commands and AI.
"""

from src.ai.brain import Brain
from .command_router import CommandRouter
from .action_executor import ActionExecutor


class Assistant:

    def __init__(self):

        self.router = CommandRouter()
        self.executor = ActionExecutor()
        self.brain = Brain()

    def handle(self, command: str):

        action, data = self.router.route(command)

        if action == "unknown":

            reply = self.brain.think(command)

            return reply, False

        result = self.executor.execute(action, data)

        if result is None:
            result = "Done."

        return result, result == "shutdown"
import unittest

from src.core.command_router import CommandRouter


class CommandRouterTests(unittest.TestCase):
    def setUp(self):
        self.router = CommandRouter()

    def test_browser_commands(self):
        self.assertEqual(self.router.route("open youtube"), ("open_youtube", None))
        self.assertEqual(self.router.route("open brave"), ("open_brave", None))

    def test_search_commands(self):
        self.assertEqual(self.router.route("search for python tutorial"), ("google_search", "python tutorial"))
        self.assertEqual(self.router.route("search youtube for lofi music"), ("youtube_search", "lofi music"))
        self.assertEqual(self.router.route("गूगल पर मौसम खोजो"), ("google_search", "मौसम"))

    def test_local_commands(self):
        self.assertEqual(self.router.route("open downloads"), ("open_folder", "downloads"))
        self.assertEqual(self.router.route("open notepad"), ("open_app", "notepad"))
        self.assertEqual(self.router.route("open vs code"), ("open_named_item", "vs code"))
        self.assertEqual(self.router.route("refresh apps"), ("refresh_launcher", None))
        self.assertEqual(self.router.route("यूट्यूब खोलो"), ("open_youtube", None))
        self.assertEqual(self.router.route("नोटपैड खोलो"), ("open_named_item", "नोटपैड"))


if __name__ == "__main__":
    unittest.main()

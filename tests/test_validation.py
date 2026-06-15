import unittest
import tkinter.messagebox as messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import get_config, update_config
from settings_gui import SettingsWindow


class MockWatcher:
    def __init__(self):
        self.watch_folder = os.path.abspath(".").replace("\\", "/")
        self.config = {
            "prefix": "US14",
            "next_number": 1,
            "watch_folder": self.watch_folder
        }
        self.on_config_change = None

    def update_watch_folder(self, folder):
        self.watch_folder = folder


class TestGUIValidation(unittest.TestCase):
    def setUp(self):
        self.original_config = get_config()
        self.watcher = MockWatcher()
        self.app = SettingsWindow(self.watcher)

        # Mock showerror to collect error messages rather than display dialogs
        self.errors = []
        messagebox.showerror = self.mock_show_error

        # Mock show_notification and root.destroy
        import watcher as w_mod
        w_mod.show_notification = lambda title, msg: None
        self.app.root.destroy = lambda: None

    def tearDown(self):
        self.app.on_close()
        update_config(self.original_config)

    def mock_show_error(self, title, message, parent=None):
        self.errors.append(message)

    def test_valid_save(self):
        self.app.prefix_var.set("TESTVALID")
        self.app.number_var.set("100")
        self.app.on_save()
        self.assertEqual(len(self.errors), 0)

        # Verify config saved correctly
        cfg = get_config()
        self.assertEqual(cfg["prefix"], "TESTVALID")
        self.assertEqual(cfg["next_number"], 100)

    def test_empty_prefix(self):
        self.app.prefix_var.set("  ")
        self.app.number_var.set("10")
        self.app.on_save()
        self.assertGreater(len(self.errors), 0)
        self.assertIn("Prefix cannot be empty", self.errors[-1])

    def test_invalid_chars_prefix(self):
        self.app.prefix_var.set("US#14")
        self.app.number_var.set("10")
        self.app.on_save()
        self.assertGreater(len(self.errors), 0)
        self.assertIn("Prefix can only contain", self.errors[-1])

    def test_negative_number(self):
        self.app.prefix_var.set("US")
        self.app.number_var.set("-5")
        self.app.on_save()
        self.assertGreater(len(self.errors), 0)
        self.assertIn("Next Number must be a positive integer", self.errors[-1])

    def test_non_integer_number(self):
        self.app.prefix_var.set("US")
        self.app.number_var.set("3.14")
        self.app.on_save()
        self.assertGreater(len(self.errors), 0)
        self.assertIn("Next Number must be a positive integer", self.errors[-1])


if __name__ == "__main__":
    unittest.main()

import unittest
import threading
import time
import os
import sys

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import get_config, update_config, get_default_screenshots_folder


class TestConfig(unittest.TestCase):
    def setUp(self):
        # Backup original configuration
        self.original_config = get_config()

    def tearDown(self):
        # Restore original configuration
        update_config(self.original_config)

    def test_get_config(self):
        config = get_config()
        self.assertIsInstance(config, dict)
        self.assertIn("prefix", config)
        self.assertIn("next_number", config)
        self.assertIn("watch_folder", config)

    def test_update_config(self):
        test_updates = {"prefix": "TCONFIG", "next_number": 99}
        updated_config = update_config(test_updates)
        self.assertEqual(updated_config["prefix"], "TCONFIG")
        self.assertEqual(updated_config["next_number"], 99)

        # Reload config and check persistence
        reloaded = get_config()
        self.assertEqual(reloaded["prefix"], "TCONFIG")
        self.assertEqual(reloaded["next_number"], 99)

    def test_default_screenshots_folder(self):
        folder = get_default_screenshots_folder()
        self.assertTrue(os.path.isabs(folder))
        # It should use forward slashes
        self.assertNotIn("\\", folder)

    def test_config_thread_safety(self):
        errors = []

        def worker():
            for _ in range(15):
                try:
                    cfg = get_config()
                    current = cfg.get("next_number", 1)
                    update_config({"next_number": current + 1})
                    time.sleep(0.005)
                except Exception as e:
                    errors.append(e)

        threads = []
        for _ in range(8):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0, f"Thread errors: {errors}")


if __name__ == "__main__":
    unittest.main()

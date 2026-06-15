import unittest
import os
import sys
import time
import shutil
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import get_config, update_config
from watcher import ScreenshotWatcher


class TestWatcher(unittest.TestCase):
    def setUp(self):
        # Backup original configuration
        self.original_config = get_config()
        self.temp_dir = tempfile.mkdtemp(prefix="watcher_test_")
        self.watch_folder = os.path.abspath(self.temp_dir).replace("\\", "/")

        # Configure watcher
        test_config = {
            "prefix": "USWATCH",
            "next_number": 1,
            "watch_folder": self.watch_folder
        }
        update_config(test_config)

        # Initialize watcher
        self.watcher = ScreenshotWatcher()
        self.watcher.start()
        # Wait a short bit for threads to start
        time.sleep(0.5)

    def tearDown(self):
        # Clean up
        self.watcher.stop()
        update_config(self.original_config)
        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass

    def test_screenshot_rename(self):
        # Write dummy screenshot file
        shot_path = os.path.join(self.watch_folder, "Screenshot_123.png")
        with open(shot_path, "wb") as f:
            f.write(b"data")

        # Wait for watcher to rename (wait up to 3 seconds)
        time.sleep(1.5)

        expected_path = os.path.join(self.watch_folder, "USWATCH_1.png")
        self.assertTrue(os.path.exists(expected_path), f"File {expected_path} was not created!")
        self.assertFalse(os.path.exists(shot_path), f"Original file {shot_path} was not deleted!")

        # Verify next number incremented in config
        cfg = get_config()
        self.assertEqual(cfg["next_number"], 2)

    def test_duplicate_name_handling(self):
        # Create target file pre-existing in directory
        pre_existing = os.path.join(self.watch_folder, "USWATCH_1.png")
        with open(pre_existing, "wb") as f:
            f.write(b"existing")

        # Create screenshot that should resolve to USWATCH_1.png
        shot_path = os.path.join(self.watch_folder, "Screenshot_456.png")
        with open(shot_path, "wb") as f:
            f.write(b"data")

        # Wait for watcher to rename
        time.sleep(1.5)

        # It should generate USWATCH_1_copy1.png since USWATCH_1.png already exists
        expected_path = os.path.join(self.watch_folder, "USWATCH_1_copy1.png")
        self.assertTrue(os.path.exists(expected_path), f"Duplicate file copy {expected_path} was not created!")

        # Verify next number still incremented in config
        cfg = get_config()
        self.assertEqual(cfg["next_number"], 2)


if __name__ == "__main__":
    unittest.main()

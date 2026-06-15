import unittest
import os
import sys
import time
import shutil
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import get_config, update_config
from watcher import ScreenshotWatcher


class TestPersistence(unittest.TestCase):
    def setUp(self):
        # Backup original configuration
        self.original_config = get_config()
        self.temp_dir = tempfile.mkdtemp(prefix="persistence_test_")
        self.watch_folder = os.path.abspath(self.temp_dir).replace("\\", "/")

        # Configure watcher
        test_config = {
            "prefix": "PERSIST",
            "next_number": 10,
            "watch_folder": self.watch_folder
        }
        update_config(test_config)

    def tearDown(self):
        update_config(self.original_config)
        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass

    def test_restart_persistence(self):
        # 1. Start initial watcher instance
        watcher1 = ScreenshotWatcher()
        watcher1.start()
        time.sleep(0.5)

        # Create first dummy file
        shot1 = os.path.join(self.watch_folder, "Screenshot1.png")
        with open(shot1, "wb") as f:
            f.write(b"data1")

        # Wait for rename
        time.sleep(1.5)

        # Should be PERSIST_10.png
        expected1 = os.path.join(self.watch_folder, "PERSIST_10.png")
        self.assertTrue(os.path.exists(expected1))

        # Check configuration has updated next_number to 11
        cfg = get_config()
        self.assertEqual(cfg["next_number"], 11)

        # Stop first watcher
        watcher1.stop()
        time.sleep(0.5)

        # 2. Start second watcher instance (simulating app restart)
        watcher2 = ScreenshotWatcher()
        watcher2.start()
        time.sleep(0.5)

        # Create second dummy file
        shot2 = os.path.join(self.watch_folder, "Screenshot2.png")
        with open(shot2, "wb") as f:
            f.write(b"data2")

        # Wait for rename
        time.sleep(1.5)

        # Should be PERSIST_11.png (continuing sequentially)
        expected2 = os.path.join(self.watch_folder, "PERSIST_11.png")
        self.assertTrue(os.path.exists(expected2))

        # Check configuration has updated next_number to 12
        cfg_final = get_config()
        self.assertEqual(cfg_final["next_number"], 12)

        # Stop second watcher
        watcher2.stop()


if __name__ == "__main__":
    unittest.main()

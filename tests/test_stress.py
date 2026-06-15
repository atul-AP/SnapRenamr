import unittest
import os
import sys
import time
import shutil
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import get_config, update_config
from watcher import ScreenshotWatcher
import watcher as watcher_mod


class TestStress(unittest.TestCase):
    def setUp(self):
        # Backup original configuration
        self.original_config = get_config()
        self.temp_dir = tempfile.mkdtemp(prefix="stress_test_")
        self.watch_folder = os.path.abspath(self.temp_dir).replace("\\", "/")

        # Configure watcher
        test_config = {
            "prefix": "STRESS",
            "next_number": 1,
            "watch_folder": self.watch_folder
        }
        update_config(test_config)

        # Mock wait_for_file_stable to bypass delay for rapid testing
        self.original_wait = watcher_mod.wait_for_file_stable
        watcher_mod.wait_for_file_stable = lambda path, **kwargs: True

        # Initialize watcher
        self.watcher = ScreenshotWatcher()
        self.watcher.start()
        time.sleep(0.5)

    def tearDown(self):
        # Clean up
        self.watcher.stop()
        watcher_mod.wait_for_file_stable = self.original_wait
        update_config(self.original_config)
        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass

    def test_500_screenshots_stress(self):
        print("[Stress Test] Generating 500 mock screenshots...")
        start_time = time.time()

        # Write 500 files rapidly
        for i in range(1, 501):
            shot_path = os.path.join(self.watch_folder, f"Screenshot_{i}.png")
            with open(shot_path, "wb") as f:
                f.write(b"stress_data")

        # Allow worker thread time to process the queue (up to 8 seconds max)
        timeout = 8.0
        poll_start = time.time()
        while time.time() - poll_start < timeout:
            cfg = get_config()
            # If the next_number reaches 501, all 500 files have been processed
            if cfg["next_number"] == 501:
                break
            time.sleep(0.1)

        elapsed = time.time() - start_time
        print(f"[Stress Test] Processed 500 files in {elapsed:.2f} seconds.")

        # Check counter consistency
        final_config = get_config()
        self.assertEqual(final_config["next_number"], 501, "Not all 500 files were processed!")

        # Verify all renamed files exist
        for i in range(1, 501):
            renamed_file = os.path.join(self.watch_folder, f"STRESS_{i}.png")
            self.assertTrue(os.path.exists(renamed_file), f"Renamed file {renamed_file} is missing!")

        print("[Stress Test] All 500 files verified sequentially.")


if __name__ == "__main__":
    unittest.main()

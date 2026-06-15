import os
import time
import queue
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification
from config import get_config, update_config


def show_notification(title, message):
    """Show a desktop notification using plyer."""
    try:
        if notification is not None:
            notification.notify(  # type: ignore
                title=title,
                message=message,
                app_name="SnapRenamr",
                timeout=3
            )
    except Exception as e:
        print(f"[Notification Error] {e}")


def wait_for_file_stable(file_path, timeout=5.0, check_interval=0.2):
    """
    Waits until a file is fully written and unlocked by its creator.
    Returns True if the file is stable and accessible, False otherwise.
    """
    if not os.path.exists(file_path):
        return False

    last_size = -1
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            if not os.path.exists(file_path):
                return False

            # Try to open the file in append/binary mode.
            # If the writing process still holds an exclusive lock, this will fail.
            with open(file_path, 'ab'):
                pass

            current_size = os.path.getsize(file_path)
            # If size hasn't changed and is non-zero, it is stable and finished
            if current_size == last_size and current_size > 0:
                return True
            last_size = current_size
        except OSError:
            # File is currently locked or inaccessible, retry
            pass

        time.sleep(check_interval)

    # Final fallback check
    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'ab'):
                pass
            return True
    except OSError:
        pass

    return False


def rename_screenshot(old_path, watcher):
    """
    Renames the screenshot at old_path using watcher's config.
    Saves the updated configuration.
    """
    folder = os.path.dirname(old_path)
    _, ext = os.path.splitext(old_path)
    ext = ext.lower()

    config = watcher.config
    prefix = config["prefix"]
    number = config["next_number"]

    # Generate proposed name
    target_name = f"{prefix}_{number}{ext}"
    target_path = os.path.join(folder, target_name)

    # Prevent overwriting existing files
    if os.path.exists(target_path):
        counter = 1
        while True:
            target_name = f"{prefix}_{number}_copy{counter}{ext}"
            target_path = os.path.join(folder, target_name)
            if not os.path.exists(target_path):
                break
            counter += 1

    # Perform the rename
    try:
        os.rename(old_path, target_path)
        print(f"[Watcher] Renamed: {os.path.basename(old_path)} -> {target_name}")

        # Show notification
        show_notification("Screenshot Renamed", f"Renamed to {target_name}")

        # Update config
        new_number = number + 1
        update_config({"next_number": new_number})
        watcher.config["next_number"] = new_number

        if watcher.on_config_change:
            watcher.on_config_change()

        return True
    except Exception as e:
        print(f"[Watcher] Failed to rename {old_path} to {target_name}: {e}")
        return False


def is_already_renamed(filename, prefix):
    """Check if the filename starts with the current prefix to prevent infinite rename loops."""
    return filename.lower().startswith(f"{prefix.lower()}_")


class ScreenshotHandler(FileSystemEventHandler):
    def __init__(self, watcher):
        super().__init__()
        self.watcher = watcher

    def on_created(self, event):
        if event.is_directory:
            return
        if self.watcher.is_paused:
            return

        file_path = event.src_path
        filename = os.path.basename(file_path)

        # Load config to check prefix
        config = get_config()
        if is_already_renamed(filename, config["prefix"]):
            return

        _, ext = os.path.splitext(file_path)
        if ext.lower() in ['.png', '.jpg', '.jpeg']:
            print(f"[Watcher] File created: {file_path}")
            self.watcher.queue.put(file_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        if self.watcher.is_paused:
            return

        file_path = event.dest_path
        filename = os.path.basename(file_path)

        # Load config to check prefix
        config = get_config()
        if is_already_renamed(filename, config["prefix"]):
            return

        _, ext = os.path.splitext(file_path)
        if ext.lower() in ['.png', '.jpg', '.jpeg']:
            print(f"[Watcher] File moved/renamed in folder: {file_path}")
            self.watcher.queue.put(file_path)


class ScreenshotWatcher:
    def __init__(self):
        self.config = get_config()
        self.watch_folder = self.config["watch_folder"]
        self.is_paused = False
        self.on_config_change = None

        self.queue = queue.Queue()
        self.worker_thread = None
        self.observer = None
        self.running = False

    def start(self):
        if self.running:
            return

        self.running = True

        # Ensure watch folder exists
        if not os.path.exists(self.watch_folder):
            try:
                os.makedirs(self.watch_folder, exist_ok=True)
            except Exception as e:
                print(f"[Watcher] Error creating folder {self.watch_folder}: {e}")

        # Start worker queue thread
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

        # Start observer
        try:
            event_handler = ScreenshotHandler(self)
            self.observer = Observer()
            self.observer.schedule(event_handler, path=self.watch_folder, recursive=False)
            self.observer.start()
            print(f"[Watcher] Observer started on: {self.watch_folder}")
        except Exception as e:
            self.observer = None
            self.is_paused = True
            print(f"[Watcher] Error: Could not monitor folder {self.watch_folder}: {e}")
            show_notification(
                "SnapRenamr Error",
                f"Monitored folder is unavailable: {self.watch_folder}"
            )

    def stop(self):
        if not self.running:
            return

        self.running = False

        # Stop watchdog observer
        if self.observer:
            self.observer.stop()
            self.observer.join()

        # Stop worker thread
        self.queue.put(None)
        if self.worker_thread:
            self.worker_thread.join()

        print("[Watcher] Observer stopped.")

    def pause(self):
        self.is_paused = True
        print("[Watcher] Paused monitoring.")

    def resume(self):
        # Reload config in case it changed (e.g. settings dialog updated it)
        self.config = get_config()

        # Handle folder change if config changed the watch folder
        if self.config["watch_folder"] != self.watch_folder:
            print("[Watcher] Watch folder changed. Reinitializing observer...")
            self.update_watch_folder(self.config["watch_folder"])

        self.is_paused = False
        print("[Watcher] Resumed monitoring.")

    def update_watch_folder(self, new_folder):
        # Stop active observer
        if self.observer:
            try:
                self.observer.stop()
                self.observer.join()
            except Exception:
                pass
            self.observer = None

        self.watch_folder = new_folder
        if not os.path.exists(self.watch_folder):
            try:
                os.makedirs(self.watch_folder, exist_ok=True)
            except Exception as e:
                print(f"[Watcher] Error creating folder {self.watch_folder}: {e}")

        try:
            event_handler = ScreenshotHandler(self)
            self.observer = Observer()
            self.observer.schedule(event_handler, path=self.watch_folder, recursive=False)
            self.observer.start()
            print(f"[Watcher] Observer restarted on new folder: {self.watch_folder}")
        except Exception as e:
            self.observer = None
            self.is_paused = True
            print(f"[Watcher] Error: Could not monitor folder {self.watch_folder}: {e}")
            show_notification(
                "SnapRenamr Error",
                f"Failed to monitor new folder: {self.watch_folder}"
            )

    def _worker(self):
        while self.running:
            try:
                # Wait for items to process
                file_path = self.queue.get(timeout=1.0)
                if file_path is None:
                    break

                # Reload config to get the absolute latest prefix and number
                self.config = get_config()
                self._process_file(file_path)
                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[Watcher Worker Error] {e}")

    def _process_file(self, file_path):
        # Wait for writing stability
        if not wait_for_file_stable(file_path):
            print(f"[Watcher] Skipped file (not stable or deleted): {file_path}")
            return

        rename_screenshot(file_path, self)

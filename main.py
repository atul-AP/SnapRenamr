from config import update_config, get_default_screenshots_folder
from watcher import ScreenshotWatcher
from tray import setup_tray


def main():
    print("[Main] Starting SnapRenamr Background Utility v1.0.0...")

    # Enforce default watch folder at startup for normal runs
    update_config({"watch_folder": get_default_screenshots_folder()})

    # Initialize the folder watcher
    watcher = ScreenshotWatcher()

    try:
        # Start watching
        watcher.start()

        # Configure and run the system tray icon
        icon = setup_tray(watcher)

        print("[Main] Utility running. Check the system tray icon.")
        # icon.run() blocks until icon.stop() is called (from tray menu Exit)
        icon.run()
    except KeyboardInterrupt:
        print("[Main] Interrupted by user. Exiting...")
    except Exception as e:
        print(f"[Main] Critical failure: {e}")
    finally:
        # Always stop watcher threads gracefully on exit
        watcher.stop()
        print("[Main] Service shutdown clean.")


if __name__ == "__main__":
    main()

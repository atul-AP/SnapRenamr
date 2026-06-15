import os
import json
import winreg
import time
import threading
import sys

if getattr(sys, 'frozen', False):
    APPLICATION_PATH = os.path.dirname(os.path.abspath(sys.executable))
else:
    APPLICATION_PATH = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(APPLICATION_PATH, "config.json")
CONFIG_LOCK = threading.RLock()


def get_default_screenshots_folder():
    """
    Detect the default Windows Screenshots folder using the registry,
    falling back to standard Pictures/Screenshots.
    """
    sub_key = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"

    # Attempt 1: Query the explicit Windows Screenshots folder GUID
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            value, _ = winreg.QueryValueEx(key, "{B7BEDE81-DF94-4682-A7D8-57A52620B86F}")
            folder = os.path.expandvars(value)
            return os.path.abspath(folder).replace("\\", "/")
    except Exception:
        pass

    # Attempt 2: Query the "My Pictures" shell folder and append "Screenshots"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            value, _ = winreg.QueryValueEx(key, "My Pictures")
            pictures_folder = os.path.expandvars(value)
            screenshots_folder = os.path.join(pictures_folder, "Screenshots")
            return os.path.abspath(screenshots_folder).replace("\\", "/")
    except Exception:
        pass

    # Fallback path if registry query fails completely
    user_profile = os.environ.get("USERPROFILE") or os.environ.get("HOMEPATH") or ""
    pictures = os.path.join(user_profile, "Pictures")
    screenshots = os.path.join(pictures, "Screenshots")
    return os.path.abspath(screenshots).replace("\\", "/")


def get_default_config():
    """Return default configuration."""
    return {
        "prefix": "US14",
        "next_number": 1,
        "watch_folder": get_default_screenshots_folder()
    }


def load_config():
    """
    Load configuration from config.json.
    Retries on file locks and prevents default reset on OS permission errors.
    """
    with CONFIG_LOCK:
        if not os.path.exists(CONFIG_FILE):
            config = get_default_config()
            _save_config_unlocked(config)
            return config

        config = None
        for attempt in range(5):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                break
            except (PermissionError, OSError) as e:
                if attempt == 4:
                    print(f"[Config] Permission error reading config: {e}")
                    return get_default_config()
                time.sleep(0.05)
            except json.JSONDecodeError as e:
                print(f"[Config] Config file corrupted, restoring defaults: {e}")
                config = get_default_config()
                _save_config_unlocked(config)
                return config

        if config is None:
            config = get_default_config()
            _save_config_unlocked(config)
            return config

        # Ensure all required keys exist
        defaults = get_default_config()
        updated = False
        for k, v in defaults.items():
            if k not in config:
                config[k] = v
                updated = True

        if updated:
            _save_config_unlocked(config)

        return config


def _save_config_unlocked(config):
    for attempt in range(5):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            return
        except (PermissionError, OSError) as e:
            if attempt == 4:
                print(f"[Config] Error writing config: {e}")
            time.sleep(0.05)


def get_config():
    """
    Thread-safe retrieval of the configuration from file.
    """
    return load_config()


def update_config(updates):
    """
    Thread-safe update of the configuration.
    """
    with CONFIG_LOCK:
        config = load_config()
        config.update(updates)
        _save_config_unlocked(config)
        return config

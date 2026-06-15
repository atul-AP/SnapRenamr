import os
import threading
from PIL import Image, ImageDraw
# pyrefly: ignore [missing-import]
import pystray
from config import get_config
from settings_gui import SettingsWindow

global_watcher = None
global_icon = None
settings_thread = None


def create_tray_icon_image():
    """Create a stylized camera tray icon on the fly."""
    size = 64
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Rounded dark slate background
    draw.rounded_rectangle([4, 4, 60, 60], radius=16, fill=(49, 50, 68, 255))

    # Main camera body (Catppuccin Blue)
    draw.rounded_rectangle([12, 22, 52, 50], radius=6, fill=(137, 180, 250, 255))

    # Top camera deck/viewfinder bump
    draw.rectangle([24, 16, 40, 22], fill=(137, 180, 250, 255))

    # Camera lens circle
    draw.ellipse([22, 26, 42, 46], fill=(30, 30, 46, 255), outline=(205, 214, 244, 255), width=3)

    # Premium pink flash dot
    draw.ellipse([43, 15, 49, 21], fill=(243, 139, 168, 255))

    return image


def update_tooltip():
    if global_icon:
        config = get_config()
        prefix = config.get("prefix", "US14")
        number = config.get("next_number", 1)
        global_icon.title = f"SnapRenamr - {prefix}_{number}"


def open_settings_action(icon, item):
    global settings_thread

    if SettingsWindow.active_instance is not None:
        try:
            # Bring existing window to front thread-safely
            SettingsWindow.active_instance.root.event_generate("<<BringToFront>>", when="tail")
            return
        except Exception:
            SettingsWindow.active_instance = None

    def run_gui():
        try:
            app = SettingsWindow(global_watcher, on_save_callback=update_tooltip)
            app.run()
        except Exception as e:
            print(f"[Tray GUI Thread Error] {e}")

    settings_thread = threading.Thread(target=run_gui, daemon=True)
    settings_thread.start()


def toggle_pause_action(icon, item):
    if global_watcher:
        if global_watcher.is_paused:
            global_watcher.resume()
        else:
            global_watcher.pause()


def get_pause_text(item):
    if global_watcher and global_watcher.is_paused:
        return "Resume Monitoring"
    return "Pause Monitoring"


def open_folder_action(icon, item):
    config = get_config()
    folder = config.get("watch_folder", "")
    if not os.path.exists(folder):
        try:
            os.makedirs(folder, exist_ok=True)
        except Exception:
            pass
    try:
        os.startfile(folder)
    except Exception as e:
        print(f"[Tray] Failed to open folder: {e}")


def exit_action(icon, item):
    if global_watcher:
        global_watcher.stop()

    # Close settings window if open
    if SettingsWindow.active_instance is not None:
        try:
            SettingsWindow.active_instance.root.event_generate("<<ExitApp>>", when="tail")
        except Exception:
            pass

    icon.stop()


def setup_tray(watcher):
    global global_watcher, global_icon
    global_watcher = watcher

    # Hook watcher's callback to refresh the tooltip on screen rename events
    watcher.on_config_change = update_tooltip

    icon_image = create_tray_icon_image()

    menu = pystray.Menu(
        pystray.MenuItem("SnapRenamr v1.0.0 (Running)", lambda: None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Open Settings", open_settings_action),
        pystray.MenuItem(get_pause_text, toggle_pause_action),
        pystray.MenuItem("Open Screenshots Folder", open_folder_action),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Exit", exit_action)
    )

    # Initialize tooltip
    config = get_config()
    prefix = config.get("prefix", "US14")
    number = config.get("next_number", 1)
    tooltip = f"SnapRenamr - {prefix}_{number}"

    icon = pystray.Icon("SnapRenamr", icon_image, tooltip, menu)
    global_icon = icon
    return icon

# SnapRenamr - User Guide

Welcome to the **SnapRenamr** user guide! This document explains how the utility works, how to configure renaming options, and how to control it using the system tray.

---

## How it Works in the Background

SnapRenamr is a lightweight desktop utility designed to monitor your Screenshots directory and rename incoming captures automatically. 

1. **Detection**: It listens for file creation or relocation events in your default Windows Screenshots directory (e.g. `C:\Users\<Name>\Pictures\Screenshots`).
2. **Stability Check**: When a new screenshot is detected, SnapRenamr waits for the image file to be completely written to disk and unlocked. This prevents file corruption.
3. **Renaming & Sequence**: Once stable, the utility renames the file using a predefined prefix (e.g. `US14`) and a sequential counter (e.g., `1`), yielding `US14_1.png`. The counter increments immediately.
4. **Collision Safeguard**: If a file with the target name already exists (e.g. `US14_1.png`), it will append copy suffixes (like `US14_1_copy1.png`) to ensure no screenshots are ever overwritten or lost.

---

## Managing Settings

You can adjust naming prefixes and counters at any time using the Settings Window.

### Opening Settings
Right-click the SnapRenamr camera icon in the Windows system tray and select **Open Settings**.

### Configuration Fields
- **Filename Prefix**: The base word or identifier for your screenshots.
  - *Constraints*: Only alphanumeric characters (letters and numbers), underscores (`_`), and hyphens (`-`) are allowed. Special characters like spaces, symbols, and slashes are rejected.
- **Next Number**: The starting sequence integer.
  - *Constraints*: Must be a positive integer greater than or equal to `1`.
- **Live Preview Card**: As you type in the Prefix and Next Number fields, the card displays a real-time preview of what the next three screenshots will be named (e.g., `US14_1.png`, `US14_2.png`, `US14_3.png`).

### Buttons
- **Reset to 1**: Quick shortcut button to reset the starting counter to `1`.
- **Save & Apply**: Saves changes to `config.json` and immediately applies them to the folder monitor.
- **Cancel**: Closes the settings window without saving changes.

> [!NOTE]
> Changes are applied in real-time. You do **not** need to restart the application or computer after clicking **Save & Apply** for the new settings to take effect.

---

## System Tray Menu Options

Right-clicking the camera icon in the system tray opens a context menu with the following controls:

- **SnapRenamr v1.0.0 (Running)**: Label indicating the active version and run state.
- **Open Settings**: Displays the settings window to customize naming options.
- **Pause Monitoring / Resume Monitoring**:
  - Click **Pause Monitoring** to temporarily stop renaming captures. Any screenshots taken while paused will retain their default Windows names.
  - Click **Resume Monitoring** to restart automated renaming.
- **Open Screenshots Folder**: Direct shortcut that launches Windows File Explorer directly in the active screenshots folder being watched.
- **Exit**: Gracefully stops the folder watcher thread, saves settings, and terminates the background process.

---

## Common Renaming Examples

### Mid-Session Prefix Swap
If you are documenting user stories for a project:
1. Set the prefix to `Sprint1` and counter to `1`.
2. Capture screenshots: they rename to `Sprint1_1.png`, `Sprint1_2.png`, `Sprint1_3.png`.
3. Open settings, change the prefix to `Sprint2`, reset counter to `1`, and click save.
4. The next screenshot will instantly name to `Sprint2_1.png`. The previous files remain unchanged.

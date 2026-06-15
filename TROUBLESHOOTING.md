# SnapRenamr - Troubleshooting Guide

This guide describes common issues you might encounter while installing or running **SnapRenamr**, along with instructions to resolve them.

---

## 1. The Tray Icon is Missing

### Cause
Windows sometimes hides inactive system tray icons in the overflow menu, or the application might not be running.

### Resolution
1. Click the **carrot icon (arrow pointing upwards `^`)** in the system tray area (lower-right of taskbar).
2. Look for the camera icon. You can drag it out of the overflow list directly onto the taskbar so that it remains visible.
3. If it is not there, check your Task Manager (**Ctrl + Shift + Esc**). In the "Details" tab, check if `SnapRenamr.exe` is running. If not, launch the application manually.

---

## 2. Screenshots are Not Being Renamed

### Cause
The watcher may be paused, the Screenshots directory might have changed, or there is an issue with the system file handler.

### Resolution
1. **Check System Tray Icon Context Menu**: Right-click the camera icon and verify it does *not* show **"Resume Monitoring"**. If it does, click it to resume monitoring.
2. **Verify the Screenshots Folder**:
   - Right-click the tray icon and select **Open Screenshots Folder**. If it opens a folder that you are not saving screenshots to, your Windows registry Screenshots directory mapping might be mismatched.
   - Standard screenshots are saved by pressing `Win + PrintScreen`. Ensure you are using this shortcut or that your capture software (like Snagit or ShareX) saves captures to the standard folder path.
3. **Registry Configuration**:
   - If Windows shell folders registry mapping is corrupted or pointing to an invalid drive, SnapRenamr will automatically fall back to `C:\Users\<Name>\Pictures\Screenshots`. Check that this directory exists and is writeable.

---

## 3. Windows Defender / SmartScreen Blocks Installation or Run

### Cause
Newly compiled or unsigned executables are sometimes flagged by Windows Defender or Application Control policies (AppLocker/WDAC) because they lack digital certificates.

### Resolution
1. **SmartScreen Bypass**:
   - When the blue pop-up window appears saying *"Windows protected your PC"*, click **More Info** under the message.
   - Click the **Run Anyway** button.
2. **Application Control Policy Block**:
   - If your PC has an active WDAC / AppLocker policy (common on corporate computers), running setup packages (like `SnapRenamrSetup.exe`) might be blocked.
   - **Bypass**: Use the portable version (`dist\SnapRenamr.exe`) instead of the installer. The portable application binary runs without registering setup stubs, avoiding common setup blocklists.
3. **Whitelisting the Folder**:
   - Add the folder where `SnapRenamr.exe` is located (e.g. `C:\Users\<Name>\AppData\Local\Programs\SnapRenamr`) to your antivirus exclusion list.

---

## 4. App Counter is Skipping Numbers or Duplicate Copies Exist

### Cause
Having multiple instances of the utility running in the background can result in race conditions where both instances attempt to rename a single file, leading to sequence skips or errors.

### Resolution
1. Open Task Manager (**Ctrl + Shift + Esc**).
2. Click the **Details** tab.
3. Locate all instances of `SnapRenamr.exe` or `python.exe` running the utility script.
4. Select each instance and click **End Task**.
5. Restart the application once from your desktop shortcut or installation directory.

---

## 5. Sequence Numbers Reset to Default or Save Fails

### Cause
If the application is running inside a write-restricted directory (like `C:\Program Files` without Admin rights), the config file cannot be updated.

### Resolution
1. Verify that `config.json` is located in a write-accessible directory.
2. When using the installer, SnapRenamr resides in local AppData (`AppData\Local\Programs\SnapRenamr`), which is fully write-accessible for standard users. If running the portable executable, ensure it is placed in a folder you have write access to (e.g., `Documents` or `Pictures`), rather than the root directory of a drive or `Program Files`.

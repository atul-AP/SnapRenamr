# SnapRenamr - Project Summary

**SnapRenamr** is a lightweight, premium Windows background utility that automatically detects and sequentially renames newly captured screenshots using a customizable prefix and running counter.

Below is a single-page summary of what has been accomplished in this project:

---

## 1. Core Application Stabilization & Rebranding
- **Unified Branding**: Rebranded the application across all windows, tray modules, notifications, and configs as **SnapRenamr v1.0.0**.
- **Registry Path Resolution**: Configured the utility to automatically query the Windows Explorer registry keys to resolve the user's default system Screenshots folder, falling back to pictures shell paths when unavailable.
- **Write Stability Locks**: Implemented a retry verification check that monitors file sizes and locks, ensuring that a screenshot is fully written to disk by Windows before any renaming attempt is executed.
- **Thread-Safety**: Integrated reentrant locks (`threading.RLock`) around all configuration reads and writes to prevent corruption under rapid screenshot capture streams.
- **Dynamic Tray & UI**: Implemented an on-the-fly, canvas-rendered system tray camera icon (no external image assets required) alongside a modern dark-themed Settings GUI for real-time config updates (no app restarts required).

---

## 2. Comprehensive Test Suite
Created a 13-test automated validation suite under `tests/` and a master runner `run_tests.py` that generates a markdown report (`test_report.md`):
- **Unit Configurations**: Verifies thread-safe config operations, defaults, and parameter merges.
- **Input Validation**: Tests bounds and character checks for filename prefixes and sequence numbers in the GUI.
- **Watcher Logic**: Confirms screenshot folder watchers work and handles duplicates by appending copy suffixes (`_copy1.png`).
- **Persistence Checks**: Assures the sequence numbers persist and resume correctly after app restarts.
- **Stress Test**: Simulates **500 screenshots** taken in rapid succession. Bypasses file stability delay to verify that the watcher handles concurrent queues safely without drops or skipped numbers in under 10 seconds.

---

## 3. Production Compilation & Packaging
- **Standalone Binary**: Compiled the application using PyInstaller into a clean, standalone, no-console Windows executable located at [`dist/SnapRenamr.exe`](file:///d:/My%20projects/automates%20screenshot%20renaming%20v1/dist/SnapRenamr.exe) (~13MB).
- **Cleanup**: Purged intermediate PyInstaller build files (e.g. the large `/build` cache) and resolved all python linter/warning highlights in test scripts.

---

## 4. Installation & Deployment setup
- **Setup Installer**: Installed Inno Setup 6 via `winget` and compiled [`installer.iss`](file:///d:/My%20projects/automates%20screenshot%20renaming%20v1/installer.iss) into a standalone setup wizard: [`installer_dist\SnapRenamrSetup.exe`](file:///d:/My%20projects/automates%20screenshot%20renaming%20v1/installer_dist/SnapRenamrSetup.exe) (~15MB).
- **Silent & Safe Execution**: Standardized setup paths to install to local user profiles (`AppData/Local/Programs`), avoiding administration checks while setting up Start Menu shortcuts, Desktop shortcuts, and auto-start registry keys on login.

---

## 5. Complete Documentation
Created dedicated markdown guides in the project workspace:
- [INSTALLATION.md](file:///d:/My%20projects/automates%20screenshot%20renaming%20v1/INSTALLATION.md): Setup wizard instructions, portable binary usage, and developer setup.
- [USER_GUIDE.md](file:///d:/My%20projects/automates%20screenshot%20renaming%20v1/USER_GUIDE.md): Detailed functionality explanations, tray menu definitions, and live preview guides.
- [TROUBLESHOOTING.md](file:///d:/My%20projects/automates%20screenshot%20renaming%20v1/TROUBLESHOOTING.md): Solutions for hidden tray icons, blocked installer policy bypasses, and multi-instance cleanup.
- [DEPLOYMENT.md](file:///d:/My%20projects/automates%20screenshot%20renaming%20v1/DEPLOYMENT.md): Technical guide for manual building and publishing instructions.

---

## 6. GitHub Integration
Configured Git version control filters ([`.gitignore`](file:///d:/My%20projects/automates%20screenshot%20renaming%20v1/.gitignore)) to keep build caches and local configs clean, and pushed the complete localized codebase to your remote GitHub repository: [atul-AP/SnapRenamr](https://github.com/atul-AP/SnapRenamr).

# SnapRenamr

A lightweight Windows desktop background utility written in Python that automatically and sequentially renames new screenshots. 

It runs silently in the system tray, monitors the Screenshots folder, detects new screenshot images instantly, waits for the file to be completely written, and renames them to a user-configured prefix and running number sequence.

---

## Features

1. **Auto-Detection**: Automatically queries the Windows Registry to find the user's default system Screenshots folder.
2. **Stable File Handling**: Detects when files are still being written by Windows or third-party capture tools and waits until files are fully unlocked before renaming.
3. **Queue-Based Sequential Processing**: Handles screenshots taken in quick succession without race conditions or skipping numbers.
4. **Duplicate Safeguard**: If the target filename (e.g. `US14_1.png`) already exists, it automatically appends a copy suffix (e.g. `US14_1_copy1.png`) to prevent accidental overwriting.
5. **System Tray Integration**:
   - **Open Settings**: Opens a custom dark-themed Settings GUI to manage the filename prefix and the next sequential starting number.
   - **Pause/Resume Monitoring**: Quickly toggle the watcher service on/off.
   - **Open Screenshots Folder**: Direct shortcut to open the active screenshots directory in Windows File Explorer.
6. **Desktop Notifications**: Pushes brief Windows toast notifications when files are renamed.

---

## Installation & Running

### 1. Set Up Virtual Environment
Open PowerShell or Command Prompt in the project directory and create a virtual environment:
```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies
Install the required packages:
```powershell
pip install -r requirements.txt
```

### 3. Run the Utility
Start the background daemon:
```powershell
python main.py
```
A custom camera icon will appear in the Windows system tray (check the hidden icons overflow area if it is not immediately visible).

---

## Packaging into a Standalone `.exe`

To compile this script into a single standalone Windows executable that runs without showing a Command Prompt console window:

1. Install PyInstaller in your virtual environment:
   ```powershell
   pip install pyinstaller
   ```

2. Package the application:
   ```powershell
   pyinstaller --onefile --noconsole --name="SnapRenamr" main.py
   ```

3. Locate your compiled executable:
   Once compilation is complete, find `SnapRenamr.exe` in the newly created `dist/` directory. You can move this executable anywhere on your system.

---

## Setup Auto-Start on Windows Login

To make the utility launch automatically in the background whenever you log into Windows:

1. Copy the compiled `SnapRenamr.exe` file (from the `dist/` folder).
2. Press `Win + R` to open the Windows "Run" dialog box.
3. Type `shell:startup` and press **Enter**. This will open the Windows **Startup** folder in File Explorer.
4. Right-click inside the folder and select **Paste Shortcut** (or drag and drop with the Alt key held down to create a shortcut to the executable).
5. The utility will now launch in the background every time Windows starts up.

---

## Managing Settings & Mid-Session Changes

You can access the Settings window at any time by right-clicking the system tray icon and selecting **Open Settings**.

### Immediate Application (No Restart Required)
When you click **Save & Apply** in the Settings window, all configurations are updated in real-time. The running folder watcher immediately detects these settings for any subsequent screenshots.

#### Example Scenario: Mid-Session Switch
Imagine you are documenting multiple user stories:
1. You start with the prefix `US4` and next number `1`.
2. You take 3 screenshots. They are automatically named:
   - `US4_1.png`
   - `US4_2.png`
   - `US4_3.png`
3. You finish User Story 4 and want to move on to User Story 5.
4. You right-click the tray icon, click **Open Settings**, change the prefix to `US5`, click **Reset to 1** (or type `1` in the Next Number field), and click **Save & Apply**.
5. The very next screenshot you take will automatically be named `US5_1.png` mid-session, without needing to restart the utility.
6. The files for `US4` are preserved exactly as they were, and progress is seamlessly moved to `US5`.

---

## Production Readiness & Pre-Release Checklist

Before distributing **SnapRenamr** to other users, please complete the following checklist:

### 1. Verification Checks
- [x] **Automated Tests**: Confirm all 13 unit, integration, stress, and persistence tests pass by running `python run_tests.py` (refer to [test_report.md](file:///d:/My%20projects/automates%20screenshot%20renaming%20v1/test_report.md)).
- [x] **Stress Load Handling**: Ensure the queue processing can handle 500 screenshots generated in rapid succession without skipped numbers or naming collisions.
- [x] **Registry Folder Fallbacks**: Validate path resolution fallback behavior when registry entries are modified or absent.
- [x] **Stability Wait**: Verify that write locks on newly created files are successfully awaited before naming attempts.

### 2. Packaging & Setup Checks
- [x] **PyInstaller Compilation**: Package the standalone executable `dist/SnapRenamr.exe` using `pyinstaller`.
- [x] **Installer Compiler Script**: Configure the Inno Setup script `installer.iss` to generate the user setup wizard.
- [x] **Installation Wizard Test**: Compile the installer setup via Inno Setup (compiles successfully, though local execution on this dev machine is restricted by Windows Application Control policy).
- [x] **Uninstallation Cleanup**: Verify that the installer uninstallation registry mappings and file removal keys are configured in `installer.iss`.

For comprehensive details on packaging commands, options, and setup configurations, refer to the [DEPLOYMENT.md](file:///d:/My%20projects/automates%20screenshot%20renaming%20v1/DEPLOYMENT.md) guide.



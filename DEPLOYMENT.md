# SnapRenamr - Deployment & Packaging Guide

This document provides production readiness guidelines, compilation instructions, and deployment options for **SnapRenamr**.

---

## 1. System Requirements
- **Operating System**: Windows 10 / 11 (64-bit).
- **Python Runtime (for source execution)**: Python 3.11+.
- **User Permissions**: Standard user privileges (administrative access is *not* required for local user installations).

---

## 2. Installation Options

### Option A: Running from Source (Developer Setup)
1. **Prepare Virtual Environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
3. **Run the App**:
   ```powershell
   python main.py
   ```

### Option B: Standalone Portable Executable
We package the application into a single standalone Windows executable `dist/SnapRenamr.exe` that contains the Python interpreter and all modules.

#### How to Build:
1. Activate the environment and install PyInstaller:
   ```powershell
   .\venv\Scripts\Activate.ps1
   pip install pyinstaller
   ```
2. Build the binary:
   ```powershell
   pyinstaller --onefile --noconsole --name="SnapRenamr" main.py
   ```
3. The executable is generated at: `dist/SnapRenamr.exe`.

#### Manually Setting up Autostart:
1. Press `Win + R`, type `shell:startup`, and press **Enter** to open the Windows Startup folder.
2. Create a shortcut to `SnapRenamr.exe` and paste it inside this folder. The app will now launch silently in the system tray when you log in.

### Option C: Production Windows Installer (Recommended for Users)
You can bundle the executable into a professional Windows Setup Wizard using **Inno Setup**.

#### How to Build:
1. Download and install [Inno Setup 6](https://jrsoftware.org/isdl.php) (free).
2. Open Inno Setup Compiler.
3. Open the `installer.iss` script located in the root folder of this project.
4. Click **Build > Compile** (or press `Ctrl + F9`).
5. The installer package will be generated at: `installer_dist/SnapRenamrSetup.exe`.

#### Installer Features:
- Installs to local user directories (`AppData\Local\Programs`) to prevent requiring Administrator access.
- Adds Start Menu and Desktop shortcuts.
- Configures a **Registry Key Run Task** to automatically launch SnapRenamr on Windows startup.
- Configures an automatic clean uninstaller.

---

## 3. Configuration & State Management
Configuration is stored in `config.json` inside the same directory as the executable/script:
```json
{
    "prefix": "US14",
    "next_number": 4,
    "watch_folder": "C:/Users/atulp/OneDrive/Pictures/Screenshots"
}
```
- **Automatic Registry Detection**: On startup, SnapRenamr queries the Windows Shell Folders registry:
  `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders`
  Specifically the GUID `{B7BEDE81-DF94-4682-A7D8-57A52620B86F}` to find the system Screenshots folder.
- **Safety Locks**: Config files are read and written using a thread-safe reentrant lock (`threading.RLock`) to prevent corruption under rapid screenshot capture loads.

---

## 4. Distribution & Publication Guidelines

Depending on your target audience, choose the appropriate method for deploying and using the compiled installer:

### Option A: Personal Use (Local Storage)
- **Action**: Keep the generated setup wizard (`installer_dist/SnapRenamrSetup.exe`) locally on your hard drive, flash drive, or personal cloud storage (e.g. OneDrive, Google Drive).
- **Execution**: Run the installer locally on your own Windows machines whenever you need to configure or update the utility.

### Option Option B: Public Use (Publishing to GitHub)
To share SnapRenamr with other users, publish it as a formal Release on GitHub:
1. **Initialize Git & Push**: Commit your workspace files and push the repository to GitHub.
2. **Draft a Release**:
   - Open your project repository page on GitHub.
   - On the right-hand panel, click **Releases > Draft a new release**.
3. **Set Version Tag**:
   - Tag version: `v1.0.0`.
   - Title: `SnapRenamr v1.0.0 - Production Release`.
4. **Upload Assets**:
   - Drag and drop the setup installer `installer_dist/SnapRenamrSetup.exe` into the release attachments box.
   - (Optional) Drag and drop the standalone portable binary `dist/SnapRenamr.exe` to allow users to run the utility without installing.
5. **Publish**: Write your release notes and click **Publish release** to make the binaries public.

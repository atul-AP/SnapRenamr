# SnapRenamr - Installation Guide

This guide details the steps required to install and set up **SnapRenamr v1.0.0** on your Windows 10 or 11 system.

---

## Installation Options

You can choose one of three installation methods depending on your preferences:
- **Option A (Recommended)**: Windows Setup Wizard Installer
- **Option B (Portable)**: Standalone Executable
- **Option C (Developer)**: Run from Python Source Code

---

## Option A: Windows Setup Wizard (Recommended)

This options bundles the utility inside a standard Windows setup installer that automatically configures shortcuts and startup automation.

### 1. Download/Obtain the Installer
Ensure you have the compiled installer executable:
`installer_dist\SnapRenamrSetup.exe`

### 2. Run the Installer
1. Double-click `SnapRenamrSetup.exe` to run the setup wizard.
2. If prompted by Windows Defender SmartScreen (due to the executable being newly compiled and unsigned), click **More Info** and then **Run Anyway**.
3. Select the folder where you want to install the application (defaults to your local program folder: `C:\Users\<YourUsername>\AppData\Local\Programs\SnapRenamr`).
4. Select the additional tasks:
   - **Create a desktop shortcut**: Adds a shortcut on your desktop.
   - **Start SnapRenamr automatically on Windows startup** (Highly Recommended): Automates the startup of the utility.
5. Click **Install**.
6. On the final page, keep **Launch SnapRenamr now** checked and click **Finish**.

---

## Option B: Standalone Portable Executable

If you do not want to install files on your computer and prefer a lightweight, portable single-binary execution.

### 1. Obtain the Executable
Get the compiled portable binary:
`dist\SnapRenamr.exe`

### 2. Run & Configure
1. Move the `SnapRenamr.exe` to a permanent folder on your PC (e.g., `C:\Tools\SnapRenamr\`).
2. Double-click the executable to launch it.
3. It will run silently in your system tray (look for the camera icon in the lower-right corner of your taskbar).
4. On its first launch, it will generate a `config.json` next to the executable to store your settings.

### 3. Setting Up Auto-Start Manually
To make the portable version launch automatically when you turn on your PC:
1. Copy the `SnapRenamr.exe` file.
2. Press `Win + R` on your keyboard, type `shell:startup`, and press **Enter** (this opens your Windows Startup folder).
3. Right-click inside the folder and select **Paste shortcut**.

---

## Option C: Running from Source (Developers)

If you wish to modify the code or run the application directly from the source code.

### Prerequisites
- Python 3.11 or newer installed on your machine.
- Pip (Python Package Index) installed.

### Setup Instructions
1. Open PowerShell or Command Prompt in the repository folder:
   ```powershell
   cd "d:\My projects\automates screenshot renaming v1"
   ```
2. Create and activate a Python virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install the required python modules:
   ```powershell
   pip install -r requirements.txt
   ```
4. Launch the application:
   ```powershell
   python main.py
   ```

---

## Verifying the Installation

To confirm that SnapRenamr is running properly:
1. **Check the System Tray**: Look for the camera icon in the bottom right corner of your Windows taskbar (check the hidden icons carrot `^` if not visible).
2. **Take a Test Screenshot**: Press the standard Windows screenshot shortcut (`Win + PrintScreen`) or capture a screenshot using your preferred snipping tool configured to save images to the default Screenshots directory.
3. **Verify Rename**: Open your system Screenshots folder (usually `Pictures/Screenshots`). The newly captured image should be automatically renamed to `US14_1.png` (or your configured prefix and starting number) within a split second, and a toast notification will pop up in Windows.

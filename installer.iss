; Inno Setup Script for SnapRenamr
; Compile this script using the Inno Setup Compiler (ISCC) to generate the setup executable.

[Setup]
AppName=SnapRenamr
AppVersion=1.0.0
DefaultDirName={userpf}\SnapRenamr
DefaultGroupName=SnapRenamr
UninstallDisplayIcon={app}\SnapRenamr.exe
Compression=lzma2
SolidCompression=yes
OutputDir=installer_dist
OutputBaseFilename=SnapRenamrSetup
PrivilegesRequired=lowest
DisableProgramGroupPage=yes
DisableDirPage=no

[Tasks]
Name: desktopicon; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked
Name: startup; Description: "Start SnapRenamr automatically on Windows startup"; GroupDescription: "Additional settings:"

[Files]
Source: "dist\SnapRenamr.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\SnapRenamr"; Filename: "{app}\SnapRenamr.exe"
Name: "{group}\Uninstall SnapRenamr"; Filename: "{uninstallexe}"
Name: "{autodesktop}\SnapRenamr"; Filename: "{app}\SnapRenamr.exe"; Tasks: desktopicon

[Registry]
; Auto-start on Windows startup (User-level Run key)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "SnapRenamr"; ValueData: """{app}\SnapRenamr.exe"""; Flags: uninsdeletevalue; Tasks: startup

[Run]
Filename: "{app}\SnapRenamr.exe"; Description: "Launch SnapRenamr now"; Flags: nowait postinstall skipifsilent

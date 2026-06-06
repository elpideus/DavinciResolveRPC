; Inno Setup script for DaVinci Resolve RPC
; Requires Inno Setup 7+ — https://jrsoftware.org/isdl.php
; Compile after running build.bat

#define AppName "DaVinci Resolve RPC"
#define AppVersion "1.0.1"
#define AppExe "DaVinciResolveRPC.exe"
#define AppPublisher "DaVinci Resolve RPC"

[Setup]
AppId={{B3F2A1D4-7C8E-4F9B-A2D1-6E3C5B8A0F7D}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={localappdata}\{#AppName}
DefaultGroupName={#AppName}
OutputDir=installer_output
OutputBaseFilename=DaVinciResolveRPC-Setup
SetupIconFile=icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
; No admin rights needed — installs per-user
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
WizardStyle=modern
; Prevent multiple instances
AppMutex=DaVinciResolveRPCMutex

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "startup"; \
    Description: "Start {#AppName} automatically when Windows starts"; \
    GroupDescription: "Startup options:"; \
    Flags:

[Files]
Source: "dist\{#AppExe}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}";           Filename: "{app}\{#AppExe}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"

[Registry]
; Add to startup when the "startup" task is selected
Root: HKCU; \
    Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
    ValueType: string; \
    ValueName: "{#AppName}"; \
    ValueData: """{app}\{#AppExe}"""; \
    Flags: uninsdeletevalue; \
    Tasks: startup

[UninstallRun]
; Kill the running process before uninstalling
Filename: "taskkill.exe"; Parameters: "/f /im {#AppExe}"; Flags: runhidden; RunOnceId: "KillApp"


[Run]
; Offer to launch immediately after install
Filename: "{app}\{#AppExe}"; \
    Description: "Launch {#AppName} now"; \
    Flags: nowait postinstall skipifsilent

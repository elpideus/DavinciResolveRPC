# DaVinci Resolve RPC

Discord Rich Presence integration for DaVinci Resolve on Windows. Runs silently in the system tray and shows your current project and timeline on your Discord profile in real time.

## Download

**[Download the latest installer](https://github.com/elpideus/DavinciResolveRPC/releases/latest/download/DaVinciResolveRPC-Setup.exe)**

![Discord Rich Presence preview](assets/discord_preview.png)

## Features

- Displays the active DaVinci Resolve project name and current timeline on Discord
- System tray icon that turns blue when Resolve is running and grey when idle
- Resets the session timer whenever you switch to a new project
- Starts automatically with Windows (optional, chosen during install)
- Single-file executable — no Python runtime required
- Per-user installation, no administrator rights needed

## Requirements

- Windows 10 or later
- DaVinci Resolve 18 or later (free or Studio edition)
- Discord desktop app running

## Installation

1. Download the latest `DaVinciResolveRPC-Setup.exe` from the [Releases](../../releases/latest) page.
2. Run the installer and follow the wizard.
3. Optionally enable **"Start automatically when Windows starts"** during setup.
4. Launch DaVinci Resolve, open a project, and check your Discord status.

## How It Works

The application polls DaVinci Resolve every 20 seconds via the official [Blackmagic Design Scripting API](https://documents.blackmagicdesign.com/DaVinciResolve/20230706-7c921a1c/DaVinci_Resolve_17_Scripting_Guide.pdf). When Resolve is detected it establishes a Discord Rich Presence connection and updates your status with:

- **Details** — current project name (e.g. `Project: My Film`)
- **State** — active timeline name (e.g. `Timeline: Assembly Cut`)
- **Elapsed time** — resets each time you switch projects

When Resolve is closed the presence is cleared automatically.

## Building From Source

### Prerequisites

- Python 3.14+
- [Inno Setup 7](https://jrsoftware.org/isdl.php) (for the installer)

### Steps

```bat
git clone https://github.com/elpideus/DavinciResolveRPC.git
cd DavinciResolveRPC
python -m venv .venv
.venv\Scripts\activate
build.bat
```

This produces `dist\DaVinciResolveRPC.exe`. To create the installer, compile `installer.iss` with Inno Setup:

```bat
"C:\Program Files (x86)\Inno Setup 7\ISCC.exe" installer.iss
```

The installer appears in `installer_output\DaVinciResolveRPC-Setup.exe`.

## License

[GNU General Public License v3.0](LICENSE)

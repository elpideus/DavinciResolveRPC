# DaVinci Resolve RPC

Discord Rich Presence integration for DaVinci Resolve on Windows. Runs silently in the system tray and shows your current project and timeline on your Discord profile in real time.

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

The application polls DaVinci Resolve every 15 seconds via the official [Blackmagic Design Scripting API](https://documents.blackmagicdesign.com/DaVinciResolve/20230706-7c921a1c/DaVinci_Resolve_17_Scripting_Guide.pdf). When Resolve is detected it establishes a Discord Rich Presence connection and updates your status with:

- **Details** — current project name (e.g. `Project: My Film`)
- **State** — active timeline name (e.g. `Timeline: Assembly Cut`)
- **Elapsed time** — resets each time you switch projects

When Resolve is closed the presence is cleared automatically.

## Building From Source

### Prerequisites

- Python 3.11+
- [Inno Setup 6](https://jrsoftware.org/isinfo.php) (for the installer)

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
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

The installer appears in `installer_output\DaVinciResolveRPC-Setup.exe`.

### Automated Releases

Pushing a tag of the form `v*` (e.g. `v1.0.0`) triggers the GitHub Actions workflow which builds the executable and installer on a Windows runner and attaches them to a GitHub Release automatically.

## Configuration

All configuration lives at the top of `resolve_rpc.py`:

| Constant | Default | Description |
|---|---|---|
| `DISCORD_CLIENT_ID` | `1511200740562047026` | Discord application client ID |
| `RESOLVE_SCRIPT_MODULE` | Standard Blackmagic path | Path to the DaVinciResolveScript module |
| `POLL_INTERVAL` | `15` | Seconds between presence updates |

## License

[GNU General Public License v3.0](LICENSE)

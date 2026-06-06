"""
Discord Rich Presence for DaVinci Resolve
Runs silently in the Windows system tray.
"""

import sys
import time
import threading
from pathlib import Path

try:
    import psutil
except ImportError:
    sys.exit("Missing dependency: pip install psutil")

try:
    from pypresence import Presence
except ImportError:
    sys.exit("Missing dependency: pip install pypresence")

try:
    from PIL import Image, ImageDraw, ImageFont
    import pystray
except ImportError:
    sys.exit("Missing dependency: pip install pystray Pillow")


VERSION = "1.0.1"
DISCORD_CLIENT_ID = "1511200740562047026"

RESOLVE_SCRIPT_MODULE = Path(
    r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"
)

POLL_INTERVAL = 20  # seconds between updates


def load_resolve_module():
    if not (RESOLVE_SCRIPT_MODULE / "DaVinciResolveScript.py").exists():
        return None
    if str(RESOLVE_SCRIPT_MODULE) not in sys.path:
        sys.path.insert(0, str(RESOLVE_SCRIPT_MODULE))
    try:
        import DaVinciResolveScript as dvr
        return dvr
    except Exception:
        return None


def is_resolve_running() -> bool:
    return any(
        p.name().lower() in ("resolve.exe", "davinci resolve.exe")
        for p in psutil.process_iter(["name"])
    )


def get_resolve_state(dvr_module) -> tuple[str, str]:
    """Returns (project_name, timeline_name). Empty strings if unavailable."""
    try:
        resolve = dvr_module.scriptapp("Resolve")
        if resolve is None:
            return "", ""
        pm = resolve.GetProjectManager()
        project = pm.GetCurrentProject()
        if project is None:
            return "", ""
        project_name = project.GetName() or "Untitled Project"
        timeline = project.GetCurrentTimeline()
        timeline_name = timeline.GetName() if timeline else ""
        return project_name, timeline_name
    except Exception:
        return "", ""


def connect_discord(client_id: str) -> "Presence | None":
    try:
        rpc = Presence(client_id)
        rpc.connect()
        return rpc
    except Exception:
        return None


def make_tray_icon(active: bool) -> Image.Image:
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer circle
    bg_color = (88, 101, 242, 255) if active else (80, 80, 80, 255)
    draw.ellipse([2, 2, size - 2, size - 2], fill=bg_color)

    # Simple "R" letterform in white
    text_color = (255, 255, 255, 255)
    try:
        font = ImageFont.truetype("arialbd.ttf", 34)
    except Exception:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), "R", font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1]), "R", fill=text_color, font=font)

    return img


def rpc_loop(stop_event: threading.Event, icon_ref: list) -> None:
    dvr_module = load_resolve_module()
    rpc = None
    session_start: float | None = None
    last_project = ""

    while not stop_event.is_set():
        resolve_running = is_resolve_running()

        if resolve_running:
            if rpc is None:
                rpc = connect_discord(DISCORD_CLIENT_ID)
                if rpc is None:
                    stop_event.wait(5)
                    continue

            if session_start is None:
                session_start = time.time()

            project_name, timeline_name = (
                ("", "") if dvr_module is None else get_resolve_state(dvr_module)
            )

            if project_name and project_name != last_project:
                session_start = time.time()
                last_project = project_name

            details = f"Project: {project_name}" if project_name else "DaVinci Resolve"
            state = f"Timeline: {timeline_name}" if timeline_name else "Editing"

            try:
                rpc.update(
                    details=details,
                    state=state,
                    start=int(session_start),
                    large_image="davinci_resolve",
                    large_text="DaVinci Resolve",
                )
                tray = icon_ref[0]
                if tray is not None:
                    tray.icon = make_tray_icon(True)
                    tray.title = f"DaVinci RPC — {project_name or 'Running'}"
            except Exception:
                rpc = None

        else:
            if rpc is not None:
                try:
                    rpc.clear()
                    rpc.close()
                except Exception:
                    pass
                rpc = None
                session_start = None
                last_project = ""

            tray = icon_ref[0]
            if tray is not None:
                tray.icon = make_tray_icon(False)
                tray.title = "DaVinci RPC — Waiting for Resolve"

        stop_event.wait(POLL_INTERVAL)

    if rpc is not None:
        try:
            rpc.clear()
            rpc.close()
        except Exception:
            pass


def main() -> None:
    stop_event = threading.Event()
    icon_ref: list = [None]

    def on_quit(icon, item):
        stop_event.set()
        icon.stop()

    tray_icon = pystray.Icon(
        "DaVinciRPC",
        make_tray_icon(False),
        "DaVinci RPC — Starting…",
        menu=pystray.Menu(
            pystray.MenuItem("DaVinci Resolve RPC", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", on_quit),
        ),
    )
    icon_ref[0] = tray_icon

    worker = threading.Thread(target=rpc_loop, args=(stop_event, icon_ref), daemon=True)
    worker.start()

    tray_icon.run()  # blocks until icon.stop() is called


if __name__ == "__main__":
    main()

# Skill: Run WakeTheDrive (GUI / System Tray Mode)

This skill teaches you how to run WakeTheDrive in graphical system-tray mode.

## Overview

When `pystray` and `Pillow` are installed, WakeTheDrive starts silently with a green icon in the system tray. All interaction happens through the tray menu — no terminal window is needed after launch. If the dependencies are absent, the program automatically falls back to CLI mode (see `.clinerules/run-cli.md`).

## Prerequisites

Install the GUI dependencies (only needed once):
```bash
pip install pystray Pillow
```

Verify they are available:
```bash
python -c "import pystray, PIL; print('GUI deps OK')"
```

## Run Commands

### Default (60-second interval)
```bash
python -m src
```

### Custom interval (e.g. 30 seconds)
```bash
python -m src --interval 30
```

Run from the **project root** (the directory containing `src/`).

## Tray Menu Items

Once running, right-click (or left-click on some platforms) the tray icon to see:

| Menu item | Description |
|---|---|
| `Drive: <letter or />` | Display-only — the target drive being kept awake |
| `File Path: <path>` | Display-only — directory where the heartbeat file is written |
| `Last Pulse: <timestamp>` | Display-only — updates each time a heartbeat is written; re-evaluate by reopening the menu |
| `Config: <path>` | Clickable — opens the JSON config file in the default OS editor |
| **Exit** | Stops the daemon thread, removes the heartbeat file, and quits |

## Executing a GUI Run (Step-by-Step)

1. Confirm you are in the project root.
2. Run `python -c "import pystray, PIL; print('OK')"` — if it prints `OK`, GUI mode will start.
3. Run `python -m src` (add `--interval N` for a custom interval).
4. Look for the green circle icon in the system tray / menu bar.
5. Open the tray menu to confirm `Last Pulse` updates at the configured interval.
6. To stop: click **Exit** in the tray menu.

## Common Failures & Fixes

| Symptom | Cause | Fix |
|---|---|---|
| No tray icon appears; CLI output shown instead | `pystray` or `Pillow` not installed | `pip install pystray Pillow` then re-run |
| No tray icon on Linux (headless / SSH session) | No display server available | GUI mode requires a desktop session; use CLI mode instead |
| Icon appears but menu doesn't open | Platform tray API quirk | Try left-click or right-click; behaviour varies by OS/desktop environment |
| `Last Pulse` timestamp does not update | Menu text is evaluated at open time — this is expected | Re-open the menu to see the latest value |
| `ModuleNotFoundError: No module named 'src'` | Running from inside `src/` | `cd` to project root and re-run |
| Program exits immediately after launch | Unhandled exception at startup | Run in a terminal to see the traceback |

## Tray UI Architecture Notes

- `TrayApp` (in `src/tray.py`) **must run on the main thread** — pystray requires it.
- `DiskPulseThread` (in `src/disk.py`) runs as a background daemon thread.
- Menu item labels are `lambda` expressions so they re-read `pulse_thread.last_pulse` each time the menu is opened.
- The icon tooltip (`WakeTheDrive`) can be updated programmatically via `TrayApp.title`.

## Notes

- `python -m src` always runs `src/__main__.py`.
- The `--interval` CLI flag takes precedence over the config file value.
- The config file is created automatically on first run and can be edited via the tray menu.
- To build a standalone binary that runs in tray mode without a terminal, see `.clinerules/build.md`.
- To run without a GUI (CLI mode), see `.clinerules/run-cli.md`.

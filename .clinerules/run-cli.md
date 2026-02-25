# Skill: Run WakeTheDrive

This skill teaches you how to run the WakeTheDrive program from source.

## Overview

WakeTheDrive is run as a Python module from the **project root** (not from `app/` or `bin/`). It requires `pystray` and `Pillow` to be installed for tray mode; without them it falls back to CLI mode.

## Prerequisites

Install runtime dependencies (only needed once):
```bash
pip install pystray Pillow
```

## Run Commands

### Default (1-second interval)
```bash
python -m app
```

### Custom interval (e.g. 30 seconds)
```bash
python -m app --interval 30
```

### Show help
```bash
python -m app --help
```

## Behaviour

- If `pystray` and `Pillow` are available: starts silently with a **green system-tray icon**. Use the tray menu to see the last pulse time and to exit.
- If `pystray` / `Pillow` are missing: runs in **CLI mode**. Press `Ctrl+C` to stop.
- On startup the program reads (or creates) a config file and writes a `WakeTheDrive.heartbeat.txt` file at the configured interval to keep the drive awake.
- On exit the `WakeTheDrive.heartbeat.txt` file is always deleted (guaranteed by a `finally` block).

## Executing a Run (Step-by-Step)

1. Confirm you are in the project root (the directory containing `app/`).
2. Ensure dependencies are installed (`pip install pystray Pillow`).
3. Run `python -m app` (add `--interval N` if a custom interval is needed).
4. Verify the program started:
   - Tray mode: a green icon appears in the system tray.
   - CLI mode: the message `Running in CLI mode. Press Ctrl+C to exit.` is printed.
5. To stop: click **Exit** in the tray menu, or press `Ctrl+C` in CLI mode.

## Common Failures & Fixes

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'app'` | Running from inside `app/` | `cd` to the project root and re-run |
| `ModuleNotFoundError: No module named 'pystray'` | Dependencies not installed | Run `pip install pystray Pillow` |
| No tray icon appears | `pystray`/`Pillow` not installed, or headless environment | Program falls back to CLI mode automatically |
| `PermissionError` writing heartbeat file | No write permission in `BASE_DIR` | Run from a directory where the user has write access |
| Program exits immediately | Unhandled exception at startup | Check the terminal output for a traceback |

## Notes

- `python -m app` always runs `app/__main__.py` via the module entry point.
- The `--interval` CLI flag takes precedence over the value stored in the config file.
- The config file lives next to the executable (frozen) or in `app/` (dev); it is created automatically on first run.
- To run the pre-built binary instead of from source, see `.clinerules/build.md`.

# WakeTheDrive — Claude Reference (CLAUDE.md)

This document is the authoritative guide for Claude when working on the WakeTheDrive codebase. Read it before making any changes.

---

## Project Overview

**WakeTheDrive** is a lightweight, cross-platform Python utility that prevents physical hard drives from spinning down. It does this by writing a tiny "heartbeat" file at a configurable interval and calling the platform-appropriate OS flush to ensure a physical disk write occurs. The app runs silently in the system tray with a green icon.

**Repository:** `https://github.com/joxon/wake-your-drive-python`
**Language:** Python 3.x
**Entry point:** `python -m src` (runs `src/__main__.py`)

---

## Project Structure

```
wake-your-drive-python/
├── src/
│   ├── __init__.py       # Package marker
│   ├── __main__.py       # Entry point, CLI arg parsing, WakeTheDrive orchestrator class
│   ├── config.py         # Platform detection, all constants & path resolution
│   ├── disk.py           # DiskPulseThread — background daemon thread, heartbeat logic
│   ├── tray.py           # TrayApp — system tray UI (pystray)
│   ├── settings.py       # Runtime config file management (load/save/ensure)
│   └── utils.py          # sleep prevention, tray availability check, icon generation
├── bin/
│   ├── requirements.txt  # pip deps for builds: pyinstaller, pystray, Pillow
│   ├── build_mac.sh      # PyInstaller build script → dist/WakeTheDrive_Mac
│   ├── build_linux.sh    # PyInstaller build script → dist/WakeTheDrive_Linux
│   └── build_exe.bat     # PyInstaller build script → dist/WakeTheDrive.exe
├── build/                # Local build artifacts (gitignored)
├── AGENTS.md             # Agent reference guide
├── CLAUDE.md             # ← this file
├── GEMINI.md             # Project mandates (absolute rules, read first)
├── README.md             # User-facing documentation
└── REQUIREMENTS.md       # Functional & technical requirements spec
```

---

## Module Responsibilities

### `src/config.py`
Single source of truth for all constants and settings. Import from here; never hardcode values elsewhere.

| Symbol | Type | Description |
|---|---|---|
| `IS_WINDOWS`, `IS_MAC`, `IS_LINUX` | `bool` | Platform flags |
| `DEFAULT_INTERVAL` | `int` | Heartbeat interval in seconds (1) |
| `HEARTBEAT_FILENAME` | `str` | `WakeTheDrive.heartbeat.txt` |
| `HEARTBEAT_FILE_PATH` | `str` | Absolute path to the heartbeat file |
| `BASE_DIR` | `str` | Directory of the executable (frozen) or `src/` (dev) |
| `DRIVE_DISPLAY` | `str` | Drive letter (Windows) or `/` (Unix) |
| `PATH_DISPLAY` | `str` | Full `BASE_DIR` for display in tray menu |
| `ES_CONTINUOUS`, `ES_SYSTEM_REQUIRED`, `FILE_ATTRIBUTE_HIDDEN` | `int\|None` | Windows-only ctypes constants |
| `F_FULLFSYNC` | `int\|None` | macOS-only fcntl constant |

### `src/disk.py` — `DiskPulseThread(threading.Thread)`
Background daemon thread. Owns all disk I/O and sleep prevention.

| Method | Description |
|---|---|
| `__init__(interval, tray_icon=None)` | Sets up interval, running flag, last_pulse |
| `run()` | Main loop: enables sleep prevention, writes heartbeat, flushes, hides file (Windows), sleeps in 1s ticks |
| `stop()` | Sets `self.running = False` to break the inner sleep loop |
| `cleanup()` | Called in `finally`: deletes heartbeat file, disables sleep prevention |

**Key invariant:** The heartbeat file deletion happens in a `finally` block — never remove this guarantee.

### `src/tray.py` — `TrayApp`
System tray UI. Must always run on the **main thread** (pystray requirement).

| Method | Description |
|---|---|
| `__init__(stop_callback, pulse_thread)` | Builds pystray menu via `build_menu_items` callable (re-evaluated on each open) |
| `run()` | Calls `self.icon.run()` — blocks main thread |
| `on_exit(icon, item)` | Calls `stop_callback()` then `icon.stop()` |
| `title` (property) | Get/set pystray icon tooltip |

Menu structure (in order):
1. `Drive: <letter or />` — display-only, disabled
2. `Last Pulse: <timestamp>` — display-only, disabled (re-evaluated each menu open via `build_menu_items` callable)
3. *(separator)*
4. `Click to open: <PATH_DISPLAY>` — opens `BASE_DIR` in the file manager
5. `Click to edit config: <CONFIG_FILE_PATH>` — opens the JSON config file in the default editor
6. `Click to exit` — stops the application

### `src/settings.py`
Runtime configuration file management. Depends on `config.py`; only imported by `__main__.py`.

| Symbol | Type | Description |
|---|---|---|
| `DEFAULT_CONFIG` | `dict` | Default values: `{"interval_seconds": 1, "heartbeat_filename": "WakeTheDrive.heartbeat.txt"}` |

| Function | Description |
|---|---|
| `load_config()` | Reads `CONFIG_FILE_PATH`, validates known keys, fills missing keys with defaults. Returns a `dict`. Never raises — logs warning on I/O or parse error. |
| `save_config(config)` | Writes `config` dict to `CONFIG_FILE_PATH` as pretty-printed JSON. Logs warning on failure. |
| `ensure_config()` | Creates the config file with defaults if it does not exist, then calls `load_config()` and returns the result. Called once at startup. |

### `src/utils.py`
Four standalone helpers.

| Function | Description |
|---|---|
| `is_tray_supported()` | Returns `True` if `pystray` and `PIL` imported successfully |
| `set_sleep_prevention(active)` | Windows: calls `SetThreadExecutionState`. macOS/Linux: currently a no-op (platform handles it differently — see roadmap) |
| `open_config_file(path)` | Opens `path` in the OS default editor. Windows: `os.startfile`. macOS: `open`. Linux: `xdg-open`. Logs warning on failure. |
| `open_file_explorer(path)` | Opens `path` in the OS default file manager. Windows: `explorer`. macOS: `open`. Linux: `xdg-open`. Logs warning on failure. |
| `create_icon_image()` | Returns a 64×64 RGBA `PIL.Image` — green circle on transparent background |

### `src/__main__.py` — `WakeTheDrive` + `main()`
Orchestrator. Parses `--interval` arg, calls `ensure_config()` to load/create the config file, creates `DiskPulseThread` and (if available) `TrayApp`, wires them together, blocks until exit. CLI `--interval` takes precedence over the config file value.

**Thread model:**
- Main thread → `TrayApp.run()` (tray mode) or `while self._running: sleep(1)` (CLI mode)
- Daemon thread → `DiskPulseThread.run()`

---

## Core Invariants (from GEMINI.md — non-negotiable)

1. **Cross-platform**: Every feature must work on Windows, macOS, and Linux, or have a safe fallback. Use `IS_WINDOWS` / `IS_MAC` / `IS_LINUX` flags from `config.py`.
2. **Zero-footprint cleanup**: `WakeTheDrive.heartbeat.txt` must be deleted in a `finally` block. Never remove that guarantee.
3. **Thread safety**: Tray UI on main thread. Disk logic on daemon thread. Never swap these.
4. **Low-level flush preserved**: `F_FULLFSYNC` on macOS must remain to guarantee hardware-level wakefulness.
5. **New dependencies**: Must be added to all three build scripts (`build_exe.bat`, `build_mac.sh`, `build_linux.sh`) and `bin/requirements.txt` simultaneously.
6. **Single-file bundle**: PyInstaller builds always use `--onefile --windowed`.
7. **Console-less production**: Builds must not spawn a console window.

---

## Development Workflow

### Run from source
```bash
pip install pystray Pillow
python -m src
# Custom interval:
python -m src --interval 30
```

### Build standalone binaries
All build scripts live in `bin/` and must be run from inside `bin/`:
```bash
cd bin

# macOS
./build_mac.sh       # → bin/dist/WakeTheDrive_Mac  (+ bin/dist/WakeTheDrive_Mac.app)

# Linux
./build_linux.sh     # → bin/dist/WakeTheDrive_Linux

# Windows
build_exe.bat        # → bin/dist/WakeTheDrive.exe
```

Each script: creates a venv, installs `bin/requirements.txt`, then runs PyInstaller with `--onefile --windowed`.

> **macOS note:** PyInstaller 6.x issues a deprecation warning that `--onefile --windowed` together on macOS will become an error in v7.0. The build currently produces both a standalone binary (`WakeTheDrive_Mac`) and a `.app` bundle (`WakeTheDrive_Mac.app`) inside `bin/dist/`. Future migration to `--onedir` mode will be required when upgrading to PyInstaller 7+.

---

## Platform Behaviour Matrix

| Feature | Windows | macOS | Linux |
|---|---|---|---|
| Sleep prevention | `SetThreadExecutionState` (ctypes) | `caffeinate` subprocess | `systemd-inhibit` |
| Disk flush | `os.fsync()` | `fcntl.F_FULLFSYNC` | `os.fsync()` |
| File hiding | `SetFileAttributesW` (hidden attribute) | Dot-prefix (`.`) | Dot-prefix (`.`) |
| GUI | `pystray` + `Pillow` | `pystray` + `Pillow` | `pystray` + `Pillow` |
| CLI fallback | ✓ | ✓ | ✓ |

> **Note:** `set_sleep_prevention()` in `utils.py` currently only implements the Windows path. macOS (`caffeinate`) and Linux (`systemd-inhibit`) subprocess calls are not yet implemented — this is a known gap.

---

## Known Gaps / Roadmap

- [ ] `set_sleep_prevention()` — implement `caffeinate` (macOS) and `systemd-inhibit` (Linux) subprocess logic.
- [ ] Dynamic tray menu updates — pystray doesn't refresh menu item text automatically; current workaround updates the icon tooltip only.
- [ ] Multiple drive targeting.
- [ ] Custom icon selection via config.
- [ ] Auto-start on system boot.
- [ ] SMART data logging during pulses.

---

## Adding a New Feature — Checklist

1. If platform-specific: add the flag branch in `config.py` first, import the flag where needed.
2. If a new dependency: add to `bin/requirements.txt` **and** all three build scripts.
3. Disk I/O changes belong in `disk.py` (`DiskPulseThread`).
4. UI changes belong in `tray.py` (`TrayApp`); remember menu items update lazily via lambdas.
5. OS-level utilities (sleep, icon) belong in `utils.py`.
6. Constants and paths belong in `config.py`.
7. Verify the heartbeat file cleanup `finally` block is intact after any change to `DiskPulseThread.run()`.
8. Test on all three platforms (or at minimum verify the conditional branches are correct).

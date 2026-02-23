# WakeTheDrive

**WakeTheDrive** is a lightweight, cross-platform utility that prevents physical hard drives from spinning down (idling) by performing periodic, low-impact disk activity — keeping your drive alive without interrupting your workflow.

---

## Features

- **Automatic Drive Targeting** — Detects and targets the physical drive it's running from.
- **Heartbeat Pulse** — Writes a tiny file (< 50 bytes) to disk at a configurable interval (default: 60 seconds).
- **Hardware-Level Flush** — Bypasses OS write caches using `fsync` (Windows/Linux) or `F_FULLFSYNC` (macOS) to ensure the physical drive head actually moves.
- **System Sleep Prevention** — Signals the OS to prevent system-wide sleep while active.
- **System Tray UI** — Runs silently in the background with a green indicator icon in the system tray.
- **Tray Menu Status** — View the target drive path and timestamp of the last successful pulse at any time.
- **Zero Footprint** — The heartbeat file (`.drive_heartbeat`) is automatically deleted on exit.
- **No Console Window** — Built to run as a true background utility.
- **CLI Fallback** — Falls back to a headless CLI mode if `pystray` is unavailable.

---

## Screenshots

> *(Tray icon appears as a green circle — indicating the drive is actively being kept awake.)*

---

## Installation

### Prerequisites

- Python 3.x
- `pip`

### Install Dependencies

```bash
pip install pystray Pillow
```

---

## Usage

### Run from Source

```bash
python -m src
```

### Custom Pulse Interval

Use the `--interval` flag to set the time (in seconds) between disk pulses:

```bash
python -m src --interval 30
```

*Default interval is **60 seconds**.*

### Tray Mode

When `pystray` and `Pillow` are installed, the app launches silently into the system tray. Right-click the green tray icon to:

- View the **target drive/path**
- View the **last pulse timestamp**
- **Quit** the application

### CLI Mode

If `pystray` or `Pillow` is not installed, the app runs in the terminal. Press `Ctrl+C` to exit.

---

## Building a Standalone Executable

Standalone binaries are built using [PyInstaller](https://pyinstaller.org/). Build scripts are located in the `bin/` directory.

### macOS

```bash
cd bin
./build_mac.sh
```

Output: `bin/dist/WakeTheDrive_Mac` (and `bin/dist/WakeTheDrive_Mac.app`)

> **Note:** PyInstaller 6.x warns that `--onefile --windowed` together on macOS is deprecated and will become an error in v7.0. The build produces both a standalone binary and a `.app` bundle. Migration to `--onedir` mode will be required when upgrading to PyInstaller 7+.

### Windows

```bat
cd bin
build_exe.bat
```

Output: `bin/dist/WakeTheDrive.exe`

### Linux

```bash
cd bin
./build_linux.sh
```

Output: `bin/dist/WakeTheDrive_Linux`

> All builds produce a **single portable binary** using `--onefile` mode. No installation required.

---

## How It Works

1. On launch, WakeTheDrive determines the directory of its own executable and sets that as the target drive.
2. A background daemon thread starts and writes a small heartbeat file (`.drive_heartbeat`) to that directory at the configured interval.
3. After each write, it calls the platform-appropriate flush function to force the OS to commit the write to the physical disk — ensuring the drive head actually moves.
4. On Windows, the heartbeat file is marked as hidden.
5. On exit (via tray menu or `Ctrl+C`), the heartbeat file is deleted and sleep prevention is released.

### Platform Details

| Feature | Windows | macOS | Linux |
| :--- | :--- | :--- | :--- |
| Sleep Prevention | `SetThreadExecutionState` | `caffeinate` | `systemd-inhibit` |
| Disk Flush | `os.fsync()` | `fcntl.F_FULLFSYNC` | `os.fsync()` |
| File Hiding | `SetFileAttributesW` | Dot-prefix (`.`) | Dot-prefix (`.`) |
| GUI Layer | `pystray` + `Pillow` | `pystray` + `Pillow` | `pystray` + `Pillow` |

---

## Project Structure

```
WakeTheDrive/
├── src/
│   ├── __main__.py     # Entry point & CLI argument parsing
│   ├── config.py       # Platform detection & app settings
│   ├── disk.py         # Background disk pulse thread
│   ├── tray.py         # System tray UI (pystray)
│   └── utils.py        # Sleep prevention & icon generation
├── bin/
│   ├── requirements.txt
│   ├── build_mac.sh
│   ├── build_linux.sh
│   └── build_exe.bat
├── REQUIREMENTS.md
└── README.md
```

---

## Dependencies

| Package | Purpose |
| :--- | :--- |
| `pystray` | System tray icon & menu management |
| `Pillow` | Tray icon image generation |
| `PyInstaller` | Bundling into a standalone executable |
| `ctypes` / `fcntl` | Low-level OS interaction (built-in) |

---

## Roadmap

- [ ] Support for targeting multiple drives simultaneously
- [ ] Custom icon selection via configuration
- [ ] Auto-start on system boot
- [ ] Logging of drive health / SMART data during pulses

---

## License

This project is open source. See `LICENSE` for details.

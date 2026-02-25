# Skill: Build WakeTheDrive

This skill teaches you how to build the WakeTheDrive project into a standalone binary.

## Overview

All build scripts live in `bin/` and **must be run from inside the `bin/` directory**. Each script:
1. Creates a Python virtual environment (`bin/venv/`) if one doesn't exist
2. Installs dependencies from `bin/requirements.txt`
3. Runs PyInstaller with `--onefile --windowed` (or `--noconsole` on Windows)
4. Outputs the binary to `bin/dist/`

## Platform Detection

Detect the OS with:
```bash
uname -s   # Linux → "Linux", macOS → "Darwin"
```
On Windows, `uname` is unavailable — use `%OS%` or check with Python: `python -c "import sys; print(sys.platform)"`.

## Build Commands

### macOS
```bash
cd bin && ./build_mac.sh
```
Output: `bin/dist/WakeTheDrive_Mac` and `bin/dist/WakeTheDrive_Mac.app`

### Linux
```bash
cd bin && ./build_linux.sh
```
Output: `bin/dist/WakeTheDrive_Linux`

### Windows
```bat
cd bin && build_exe.bat
```
Output: `bin/dist/WakeTheDrive.exe`

## Build Verification

After building, confirm the binary exists:

```bash
# macOS
ls -lh bin/dist/WakeTheDrive_Mac

# Linux
ls -lh bin/dist/WakeTheDrive_Linux

# Windows (PowerShell)
Get-Item bin\dist\WakeTheDrive.exe
```

## Executing a Build (Step-by-Step)

1. Detect the current platform.
2. `cd` into `bin/` before running any build command — PyInstaller paths are relative to that directory.
3. Run the platform-appropriate build script.
4. Verify the output binary exists in `bin/dist/`.
5. Report the binary path and file size to the user.

## Common Failures & Fixes

| Symptom | Cause | Fix |
|---|---|---|
| `python3: command not found` | Python 3 not on PATH | Install Python 3 or use `python` instead |
| `pip install` fails | No internet / proxy | Check connectivity; try `pip install --no-cache-dir -r requirements.txt` |
| PyInstaller `ModuleNotFoundError` | Missing hidden import | Add `--hidden-import=<module>` to the PyInstaller invocation in the script |
| `Permission denied` on `build_mac.sh` or `build_linux.sh` | Script not executable | Run `chmod +x bin/build_mac.sh` or `chmod +x bin/build_linux.sh` |
| Build output missing | PyInstaller error mid-build | Re-run the script; check the PyInstaller log printed to stdout |
| macOS deprecation warning about `--onefile --windowed` | PyInstaller 6.x behaviour | Safe to ignore until PyInstaller 7+ is adopted |

## Dependencies

Defined in `bin/requirements.txt`:
```
pyinstaller
pystray
Pillow
```

If you add a new Python dependency to the project, add it to `bin/requirements.txt` **and** to all three build scripts (they all call `pip install -r requirements.txt`, so updating the file is sufficient).

## Notes

- `bin/venv/` is created inside `bin/` — do not run the scripts from the project root or `app/`.
- `build/` at the project root is gitignored local build scratch space; the actual distributable artifacts are in `bin/dist/`.
- PyInstaller spec/work files (`*.spec`, `build/`) inside `bin/` are also gitignored.

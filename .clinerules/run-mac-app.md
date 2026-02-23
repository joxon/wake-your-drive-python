# Skill: Run WakeTheDrive (macOS App Bundle)

This skill teaches you how to run WakeTheDrive as a native macOS `.app` bundle.

## Overview

The macOS build produces both a standalone binary (`WakeTheDrive_Mac`) and a `.app` bundle (`WakeTheDrive_Mac.app`) inside `bin/dist/`. The `.app` can be launched from Finder like any native Mac application or via the `open` command from the terminal.

## Prerequisites

The `.app` bundle must be built first. If `bin/dist/WakeTheDrive_Mac.app` does not exist, build it:
```bash
cd bin && ./build_mac.sh
```
See `.clinerules/build.md` for full build instructions.

## Launch Commands

### From the terminal
```bash
open bin/dist/WakeTheDrive_Mac.app
```

### From Finder
Double-click `WakeTheDrive_Mac.app` inside `bin/dist/`.

### Move to Applications folder (optional, for permanent install)
```bash
cp -r bin/dist/WakeTheDrive_Mac.app /Applications/WakeTheDrive.app
open /Applications/WakeTheDrive.app
```

## Verifying It Is Running

After launch, a **green circle icon** appears in the macOS menu bar (top-right). If no icon appears within a few seconds, check for errors:

```bash
# Confirm the process is running
ps aux | grep -i wakethedrive | grep -v grep

# View crash logs if it exited immediately
log show --predicate 'process == "WakeTheDrive_Mac"' --last 5m
```

## Stopping the App

Click the green icon in the menu bar, then choose **Exit** from the menu.

If the menu bar icon is not visible, kill the process:
```bash
pkill -f WakeTheDrive_Mac
```

## macOS Gatekeeper / Security Issues

Because the app is unsigned, macOS may block it on first launch.

### Symptom
> "WakeTheDrive_Mac.app" cannot be opened because the developer cannot be verified.

### Fix — Remove quarantine attribute
```bash
xattr -cr bin/dist/WakeTheDrive_Mac.app
```
Then re-launch with `open bin/dist/WakeTheDrive_Mac.app`.

### Alternative fix — System Settings
1. Attempt to open the app (it will be blocked).
2. Open **System Settings → Privacy & Security**.
3. Scroll to the bottom and click **"Open Anyway"** next to the WakeTheDrive entry.

## Executing a Mac App Run (Step-by-Step)

1. Confirm `bin/dist/WakeTheDrive_Mac.app` exists (`ls bin/dist/`).
2. Remove any quarantine attribute: `xattr -cr bin/dist/WakeTheDrive_Mac.app`
3. Launch: `open bin/dist/WakeTheDrive_Mac.app`
4. Confirm the green icon appears in the menu bar.
5. Open the menu to verify `Last Pulse` updates at the configured interval.
6. To stop: click **Exit** in the menu, or run `pkill -f WakeTheDrive_Mac`.

## Common Failures & Fixes

| Symptom | Cause | Fix |
|---|---|---|
| "Cannot be opened — developer cannot be verified" | Gatekeeper quarantine | Run `xattr -cr bin/dist/WakeTheDrive_Mac.app` |
| No menu bar icon after launch | App crashed at startup | Run `log show --predicate 'process == "WakeTheDrive_Mac"' --last 2m` to see the error |
| App opens a terminal window | Built without `--windowed` flag | Rebuild with `./build_mac.sh` (it already includes `--windowed`) |
| `open: can't open file` | Path is wrong or app not built yet | Verify `bin/dist/WakeTheDrive_Mac.app` exists; rebuild if missing |
| Duplicate instances running | Launched multiple times | Run `pkill -f WakeTheDrive_Mac` to kill all instances, then re-launch once |
| Menu bar icon disappears after sleep | macOS killed the process | Re-launch the app; consider adding it to Login Items for persistence |

## Notes

- The `.app` bundle and the standalone binary (`WakeTheDrive_Mac`) are separate artifacts — both live in `bin/dist/` after the build. The `.app` is preferred for day-to-day use.
- The app is **not code-signed**. This means Gatekeeper will block it on first open; the `xattr -cr` fix is a one-time step per machine.
- To have the app start automatically on login: **System Settings → General → Login Items → Add** and select `WakeTheDrive_Mac.app`.
- To run from source instead of the built binary, see `.clinerules/run-gui.md` or `.clinerules/run-cli.md`.

# WakeTheDrive Mandates

This document takes absolute precedence over general workflows. All changes to the WakeTheDrive codebase must adhere to these foundational rules.

## 1. Cross-Platform Integrity
- **No Platform Lock-in**: Every feature must have a functional implementation or a safe fallback for Windows, macOS, and Linux.
- **Abstraction First**: Use the `IS_WINDOWS`, `IS_MAC`, and `IS_LINUX` flags to handle platform-specific logic within shared functions.
- **Low-Level Precision**: Platform-specific disk flushing (like `F_FULLFSYNC` on macOS) must be preserved to ensure hardware-level wakefulness.

## 2. Engineering Standards
- **Zero-Footprint Cleanup**: The heartbeat file (`.drive_heartbeat`) must be deleted in a `finally` block or signal handler. No temporary files should persist after exit.
- **Thread Safety**: The system tray (UI) must run on the main thread, while the disk pulse logic must run on a background daemon thread to prevent UI freezing.
- **Dependency Management**: Any new library must be added to all three build scripts (`build_exe.bat`, `build_mac.sh`, `build_linux.sh`) immediately.
- **Console-Less Execution**: The application must default to "Windowed/No-Console" mode in production builds to remain unobtrusive.

## 3. UI/UX Mandates
- **Tray-First Interaction**: All status updates (Last Pulse, Target Drive) must be accessible via the system tray menu.
- **Hover Clarity**: The tray icon's tooltip/title must always display the time of the last successful pulse.
- **Visual Feedback**: The tray icon should provide a clear visual indicator that the tool is active (e.g., a green light/icon).

## 4. Build Protocol
- **Single-File Bundle**: Always use the `--onefile` flag in PyInstaller to ensure the tool remains a portable, single-binary utility.
- **Architecture Aware**: Build scripts must respect the target OS naming conventions (e.g., `.exe` for Windows, `_Mac` for macOS).

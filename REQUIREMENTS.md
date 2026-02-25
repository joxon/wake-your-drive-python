# WakeTheDrive Requirements & Specification

A cross-platform utility designed to prevent physical hard drives from spinning down (idling) by performing periodic, low-impact disk activity.

## 1. Functional Requirements
- **Automatic Targeting**: The application must identify and target the physical drive from which it is currently executing.
- **Pulse Mechanism**: Must perform a write operation to a "heartbeat" file at a configurable interval (default: 1 second).
- **Physical Sync**: Must bypass OS write caches to ensure the physical drive head moves/activity occurs (e.g., `fsync` on Windows/Linux, `F_FULLFSYNC` on macOS).
- **System Sleep Prevention**: Must inform the OS to prevent system-wide sleep while the application is active.
- **Background Operation**: Must run without a persistent terminal or console window.
- **User Interface**:
    - **System Tray**: Must display an icon in the system tray (Windows/macOS/Linux).
    - **Status Visibility**: Users must be able to view the target drive and the timestamp of the last successful pulse via a tray menu.
    - **Graceful Exit**: Users must be able to terminate the program via the tray menu, ensuring cleanup of temporary files.

## 2. Technical Specifications

### Platform-Specific Implementations
| Feature | Windows | macOS | Linux |
| :--- | :--- | :--- | :--- |
| **API for Sleep** | `SetThreadExecutionState` | `caffeinate` | `systemd-inhibit` |
| **Disk Flush** | `os.fsync()` | `fcntl.F_FULLFSYNC` | `os.fsync()` |
| **GUI Layer** | `pystray` + `Pillow` | `pystray` + `Pillow` | `pystray` + `Pillow` |

### File System Impact
- **File Name**: `WakeTheDrive.heartbeat.txt`
- **Size**: < 50 bytes per pulse.
- **Cleanup**: The file must be deleted immediately upon application exit.

## 3. Build & Distribution
- **Single Executable**: The application must be bundled into a single standalone binary for each OS using `PyInstaller`.
- **Target OS**: 
    - Windows (.exe)
    - macOS (.app / binary)
    - Linux (ELF binary)

## 4. Dependencies
- **Language**: Python 3.x
- **Libraries**:
    - `pystray`: System tray management.
    - `Pillow`: Icon generation/manipulation.
    - `PyInstaller`: Executable bundling.
    - `ctypes` / `fcntl`: Low-level OS interaction.

## 5. Future Considerations (Backlog)
- [ ] Support for targeting multiple drives simultaneously.
- [ ] Custom icon selection via configuration.
- [ ] Auto-start on system boot.
- [ ] Logging of drive health/SMART data during pulses.

import os
import time
from datetime import datetime
import threading

from app.constants import (
    APP_NAME,
    BASE_DIR,
    HEARTBEAT_FILENAME,
    PATH_DISPLAY,
    IS_MAC,
    IS_LINUX,
    IS_WINDOWS,
)

HEARTBEAT_FILE_PATH = os.path.join(BASE_DIR, HEARTBEAT_FILENAME)

# Windows-specific constants for sleep prevention
if IS_WINDOWS:
    import ctypes
    _ES_CONTINUOUS = 0x80000000
    _ES_SYSTEM_REQUIRED = 0x00000001
else:
    ctypes = None  # type: ignore[assignment]
    _ES_CONTINUOUS = None
    _ES_SYSTEM_REQUIRED = None

# macOS-specific constant for hardware-level disk flush
if IS_MAC:
    import fcntl
    _F_FULLFSYNC = fcntl.F_FULLFSYNC
else:
    fcntl = None  # type: ignore[assignment]
    _F_FULLFSYNC = None


def set_sleep_prevention(active=True):
    """
    Prevents or allows the system to sleep.
    (Windows only)
    """
    # Windows only: tell the OS not to sleep or turn off the display while we're running.
    # _ES_SYSTEM_REQUIRED keeps the system awake; _ES_CONTINUOUS makes the state sticky so
    # it persists until explicitly cleared (called again with just _ES_CONTINUOUS).
    if IS_WINDOWS:
        try:
            state = (_ES_CONTINUOUS | _ES_SYSTEM_REQUIRED) if active else _ES_CONTINUOUS
            ctypes.windll.kernel32.SetThreadExecutionState(state)
        except Exception as e:
            print(f"Failed to set sleep prevention state: {e}")


class DiskPulseThread(threading.Thread):
    def __init__(self, interval, tray_icon=None):
        super().__init__(daemon=True)
        self.interval = interval
        self.tray_icon = tray_icon
        self.running = True
        self.last_pulse = "Never"

    def run(self):
        """The background task that keeps the drive awake."""
        set_sleep_prevention(True)
        try:
            while self.running:
                now = datetime.now()
                now_str = now.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    # NOTE: Do NOT set the Windows hidden-file attribute (FILE_ATTRIBUTE_HIDDEN /
                    # SetFileAttributesW) on the heartbeat file.  Windows' C runtime opens files
                    # with _O_CREAT | _O_TRUNC, which returns ERROR_ACCESS_DENIED when the target
                    # file already has the hidden attribute set.  The result is a silent
                    # PermissionError on every pulse after the first, so the file is created once
                    # and never updated again.
                    with open(HEARTBEAT_FILE_PATH, "w") as f:
                        f.write(f"Last pulse: {now_str}\n")
                        f.flush()
                        # Force a hardware-level flush so the drive head physically moves.
                        # On macOS, os.fsync() only flushes to the kernel's unified buffer
                        # cache; the drive may not receive the write at all.  F_FULLFSYNC
                        # issues a physical flush (equivalent to a drive FLUSH CACHE command),
                        # which is the only guarantee that the platter/head actually activates.
                        # Fall back to os.fsync() if fcntl is unavailable for any reason.
                        # On all other platforms, os.fsync() is sufficient.
                        if IS_MAC:
                            try:
                                fcntl.fcntl(f.fileno(), _F_FULLFSYNC)
                            except Exception:
                                os.fsync(f.fileno())
                        else:
                            os.fsync(f.fileno())

                    self.last_pulse = now_str
                    print(f"[{now_str}] Pulse sent to {PATH_DISPLAY}")
                    if self.tray_icon:
                        self.tray_icon.title = f"{APP_NAME}: Last pulse at {now_str}"
                        # On Windows, update_menu() sends a Win32 message that must be
                        # processed by the main thread - calling it from a background
                        # thread causes a deadlock. The menu lambda already re-reads
                        # last_pulse on every open, so no update_menu() is needed there.
                        # On macOS/Linux, pystray caches the NSMenu/GTK menu and needs
                        # an explicit nudge to pick up the new label text.
                        if IS_MAC or IS_LINUX:
                            self.tray_icon.update_menu()

                except Exception as e:
                    print(f"Error during disk pulse: {e}")

                # Sleep in small increments to stay responsive to 'running' flag
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
        finally:
            self.cleanup()

    def stop(self):
        self.running = False

    def cleanup(self):
        if os.path.exists(HEARTBEAT_FILE_PATH):
            try:
                os.remove(HEARTBEAT_FILE_PATH)
            except Exception as e:
                print(f"Error cleaning up heartbeat file: {e}")
        set_sleep_prevention(False)
        print("Disk pulse thread stopped and cleaned up.")

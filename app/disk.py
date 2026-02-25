import os
import time
from datetime import datetime
import threading

from app.config import (
    APP_NAME,
    HEARTBEAT_FILE_PATH,
    PATH_DISPLAY,
    IS_MAC,
    IS_WINDOWS,
    F_FULLFSYNC,
    FILE_ATTRIBUTE_HIDDEN,
    ES_CONTINUOUS,
    ES_SYSTEM_REQUIRED,
)


def set_sleep_prevention(active=True):
    """
    Prevents or allows the system to sleep.
    (Windows only)
    """
    if IS_WINDOWS:
        try:
            import ctypes
            state = (ES_CONTINUOUS | ES_SYSTEM_REQUIRED) if active else ES_CONTINUOUS
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
                    with open(HEARTBEAT_FILE_PATH, "w") as f:
                        f.write(f"Last pulse: {now_str}\n")
                        f.flush()
                        if IS_MAC:
                            try:
                                import fcntl
                                fcntl.fcntl(f.fileno(), F_FULLFSYNC)
                            except Exception:
                                os.fsync(f.fileno())
                        else:
                            os.fsync(f.fileno())

                    if IS_WINDOWS:
                        try:
                            import ctypes
                            ctypes.windll.kernel32.SetFileAttributesW(
                                HEARTBEAT_FILE_PATH, FILE_ATTRIBUTE_HIDDEN
                            )
                        except Exception:
                            pass

                    self.last_pulse = now_str
                    print(f"[{now_str}] Pulse sent to {PATH_DISPLAY}")
                    if self.tray_icon:
                        self.tray_icon.title = f"{APP_NAME}: Last pulse at {now_str}"
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

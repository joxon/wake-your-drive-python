
import os
import time
from datetime import datetime
import threading

from src.config import (
    HEARTBEAT_FILE_PATH,
    PATH_DISPLAY,
    IS_MAC,
    IS_WINDOWS,
    F_FULLFSYNC,
    FILE_ATTRIBUTE_HIDDEN,
)
from src.utils import set_sleep_prevention


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
                now = datetime.now().strftime("%H:%M:%S")
                try:
                    with open(HEARTBEAT_FILE_PATH, "w") as f:
                        f.write(f"Pulse: {now}")
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

                    self.last_pulse = now
                    print(f"[{now}] Pulse sent to {PATH_DISPLAY}")
                    if self.tray_icon:
                        self.tray_icon.title = f"WakeTheDrive: Last pulse at {now}"
                        # This is a bit of a hack to update the menu item text
                        # pystray doesn't have a direct way to update menu items dynamically
                        # A better approach would be to recreate the menu on change,
                        # but for this simple case, we can live with the title update.

                except Exception as e:
                    print(f"Error during disk pulse: {e}")

                # Sleep in small increments to stay responsive to 'running' flag
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
        finally:
            self.cleanup()C)
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

                    self.last_pulse = now
                    print(f"[{now}] Pulse sent to {DRIVE_INFO}")
                    if self.tray_icon:
                        self.tray_icon.title = f"WakeTheDrive: Last pulse at {now}"
                        # This is a bit of a hack to update the menu item text
                        # pystray doesn't have a direct way to update menu items dynamically
                        # A better approach would be to recreate the menu on change,
                        # but for this simple case, we can live with the title update.

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

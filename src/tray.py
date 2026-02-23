
from src.utils import is_tray_supported, create_icon_image
from src.config import DRIVE_DISPLAY, PATH_DISPLAY

if is_tray_supported():
    import pystray

class TrayApp:
    def __init__(self, stop_callback, pulse_thread):
        if not is_tray_supported():
            self.icon = None
            return

        self.stop_callback = stop_callback
        self.pulse_thread = pulse_thread

        menu = pystray.Menu(
            pystray.MenuItem(lambda text: f"Drive: {DRIVE_DISPLAY}", None, enabled=False),
            pystray.MenuItem(lambda text: f"File Path: {PATH_DISPLAY}", None, enabled=False),
            pystray.MenuItem(
                lambda text: f"Last Pulse: {self.pulse_thread.last_pulse}",
                None,
                enabled=False,
            ),
            pystray.MenuItem("Exit", self.on_exit),
        )

        self.icon = pystray.Icon(
            "WakeTheDrive", create_icon_image(), "WakeTheDrive", menu
        )

    def run(self):
        if self.icon:
            print("System Tray icon started. Right-click to exit.")
            self.icon.run()

    def on_exit(self, icon, item):
        self.stop_callback()
        if self.icon:
            self.icon.stop()

    @property
    def title(self):
        if self.icon:
            return self.icon.title
        return ""

    @title.setter
    def title(self, text):
        if self.icon:
            self.icon.title = text

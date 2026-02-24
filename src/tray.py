from src.utils import is_tray_supported, create_icon_image, open_config_file, open_file_explorer
from src.config import APP_NAME, DRIVE_DISPLAY, PATH_DISPLAY, CONFIG_FILE_PATH, BASE_DIR

if is_tray_supported():
    import pystray

class TrayApp:
    def __init__(self, stop_callback, pulse_thread):
        if not is_tray_supported():
            self.icon = None
            return

        self.stop_callback = stop_callback
        self.pulse_thread = pulse_thread

        def build_menu_items():
            return (
                pystray.MenuItem(f"Drive: {DRIVE_DISPLAY}", None, enabled=False),
                pystray.MenuItem(
                    f"Last Pulse: {self.pulse_thread.last_pulse}",
                    None,
                    enabled=False,
                ),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem(
                    f"Click to open: {PATH_DISPLAY}",
                    lambda icon, item: open_file_explorer(BASE_DIR),
                ),
                pystray.MenuItem(
                    f"Click to edit config: {CONFIG_FILE_PATH}",
                    lambda icon, item: open_config_file(CONFIG_FILE_PATH),
                ),
                pystray.MenuItem("Click to exit", self.on_exit),
            )

        self.icon = pystray.Icon(
            APP_NAME, create_icon_image(), APP_NAME, pystray.Menu(build_menu_items)
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

import subprocess

from app.config import APP_NAME, IS_WINDOWS, IS_MAC, DRIVE_DISPLAY, PATH_DISPLAY, CONFIG_FILE_PATH, BASE_DIR

# Optional: System Tray support
try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_SUPPORT = True
except ImportError:
    TRAY_SUPPORT = False


def is_tray_supported() -> bool:
    return TRAY_SUPPORT


def create_icon_image():
    """
    Generates a simple 64x64 icon (Green circle for 'Active').
    Requires PIL/Pillow.
    """
    if not TRAY_SUPPORT:
        return None
    width, height = 64, 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)
    # Draw a bright green circle
    dc.ellipse((10, 10, 54, 54), fill=(0, 255, 0), outline=(255, 255, 255))
    return image


def open_config_file(path: str) -> None:
    """
    Opens the given file path in the OS default application.
    - Windows: os.startfile()
    - macOS:   'open' command
    - Linux:   'xdg-open' command
    Silently logs a warning on failure.
    """
    try:
        if IS_WINDOWS:
            import os as _os
            _os.startfile(path)  # type: ignore[attr-defined]
        elif IS_MAC:
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception as e:
        print(f"[{APP_NAME}] Warning: could not open config file: {e}")


def open_file_explorer(path: str) -> None:
    """
    Opens the given directory path in the OS default file manager.
    - Windows: os.startfile()
    - macOS:   'open' command
    - Linux:   'xdg-open' command
    Silently logs a warning on failure.
    """
    try:
        if IS_WINDOWS:
            import os as _os
            _os.startfile(path)  # type: ignore[attr-defined]
        elif IS_MAC:
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception as e:
        print(f"[{APP_NAME}] Warning: could not open file explorer: {e}")

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
                    lambda item: f"Last Pulse: {self.pulse_thread.last_pulse}",
                    None,
                    enabled=False,
                ),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem(
                    f"Open folder: {PATH_DISPLAY}",
                    lambda icon, item: open_file_explorer(BASE_DIR),
                ),
                pystray.MenuItem(
                    f"Edit config: {CONFIG_FILE_PATH}",
                    lambda icon, item: open_config_file(CONFIG_FILE_PATH),
                ),
                pystray.MenuItem("Exit", self.on_exit),
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

    def update_menu(self):
        """
        Force pystray to rebuild the menu from the build_menu_items callable.
        Safe to call from a background thread on macOS and Linux.
        Do NOT call from a background thread on Windows. use the title setter instead.
        """
        if self.icon:
            try:
                self.icon.update_menu()
            except Exception:
                pass

    @title.setter
    def title(self, text):
        if self.icon:
            self.icon.title = text

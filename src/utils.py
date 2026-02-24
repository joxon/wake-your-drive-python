
import subprocess

from src.config import APP_NAME, IS_WINDOWS, IS_MAC, IS_LINUX, ES_CONTINUOUS, ES_SYSTEM_REQUIRED

# Optional: System Tray support
try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_SUPPORT = True
except ImportError:
    TRAY_SUPPORT = False


def is_tray_supported():
    return TRAY_SUPPORT


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


def create_icon_image():
    """
    Generates a simple 64x64 icon (Green circle for 'Active').
    Requires PIL/Pillow.
    """
    if not is_tray_supported():
        return None
    width, height = 64, 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)
    # Draw a bright green circle
    dc.ellipse((10, 10, 54, 54), fill=(0, 255, 0), outline=(255, 255, 255))
    return image

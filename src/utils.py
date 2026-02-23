
from src.config import IS_WINDOWS, ES_CONTINUOUS, ES_SYSTEM_REQUIRED

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

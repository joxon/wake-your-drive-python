import os
import sys

# Platform flags
IS_WINDOWS = os.name == 'nt'
IS_MAC = sys.platform == 'darwin'
IS_LINUX = sys.platform.startswith('linux')

# Application constants
APP_NAME = "WakeTheDrive"
DEFAULT_INTERVAL = 1
HEARTBEAT_FILENAME = f"{APP_NAME}.heartbeat.txt"

# Determine base directory
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# User-friendly path display (used by disk.py and tray.py)
PATH_DISPLAY = BASE_DIR

# Config file path (used by config.py and tray.py)
CONFIG_FILE_PATH = os.path.join(BASE_DIR, f"{APP_NAME}.config.json")
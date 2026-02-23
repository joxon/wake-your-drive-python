
import os
import sys

# Platform-specific constants
IS_WINDOWS = os.name == 'nt'
IS_MAC = sys.platform == 'darwin'
IS_LINUX = sys.platform.startswith('linux')

# Windows-specific constants for sleep prevention
if IS_WINDOWS:
    import ctypes
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    FILE_ATTRIBUTE_HIDDEN = 0x02
else:
    ES_CONTINUOUS = None
    ES_SYSTEM_REQUIRED = None
    FILE_ATTRIBUTE_HIDDEN = None

# macOS-specific constants
if IS_MAC:
    import fcntl
    F_FULLFSYNC = fcntl.F_FULLFSYNC
else:
    F_FULLFSYNC = None

# Application settings
DEFAULT_INTERVAL = 1
HEARTBEAT_FILENAME = "WakeYourDrive.heartbeat.txt"

# Determine base directory
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Determine user-friendly drive and path info
if IS_WINDOWS:
    DRIVE_DISPLAY, _ = os.path.splitdrive(BASE_DIR)
    PATH_DISPLAY = BASE_DIR
else:
    # On Unix-like systems, a "drive" isn't as distinct.
    # We'll show the root as the "Drive" and the full path as "Path".
    DRIVE_DISPLAY = "/"
    PATH_DISPLAY = BASE_DIR

HEARTBEAT_FILE_PATH = os.path.join(BASE_DIR, HEARTBEAT_FILENAME)

# Config file settings
CONFIG_FILENAME = "WakeYourDrive.config.json"
CONFIG_FILE_PATH = os.path.join(BASE_DIR, CONFIG_FILENAME)

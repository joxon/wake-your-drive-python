import json
import os

from app.config import APP_NAME, CONFIG_FILE_PATH, DEFAULT_INTERVAL, HEARTBEAT_FILENAME

# Default config values
DEFAULT_CONFIG = {
    "interval_seconds": DEFAULT_INTERVAL,
    "heartbeat_filename": HEARTBEAT_FILENAME,
}


def load_config() -> dict:
    """
    Load config from CONFIG_FILE_PATH.
    Missing keys are filled with defaults.
    If the file is missing or corrupt, returns all defaults without raising.
    """
    config = dict(DEFAULT_CONFIG)
    if not os.path.isfile(CONFIG_FILE_PATH):
        return config
    try:
        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Merge: only accept recognised keys; fall back to default for missing ones
        if isinstance(data.get("interval_seconds"), int):
            config["interval_seconds"] = data["interval_seconds"]
        if isinstance(data.get("heartbeat_filename"), str) and data["heartbeat_filename"]:
            config["heartbeat_filename"] = data["heartbeat_filename"]
    except (json.JSONDecodeError, OSError, ValueError) as e:
        print(f"[{APP_NAME}] Warning: could not read config file '{CONFIG_FILE_PATH}': {e}")
    return config


def save_config(config: dict) -> None:
    """
    Write config dict to CONFIG_FILE_PATH as pretty-printed JSON.
    Logs a warning on failure (e.g. permission denied) without raising.
    """
    try:
        with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
            f.write("\n")
    except OSError as e:
        print(f"[{APP_NAME}] Warning: could not write config file '{CONFIG_FILE_PATH}': {e}")


def ensure_config() -> dict:
    """
    If the config file does not exist, create it with defaults.
    Then load and return the effective config.
    """
    if not os.path.isfile(CONFIG_FILE_PATH):
        save_config(DEFAULT_CONFIG)
        print(f"[{APP_NAME}] Created default config: {CONFIG_FILE_PATH}")
    return load_config()

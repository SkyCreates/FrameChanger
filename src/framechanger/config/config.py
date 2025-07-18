import os
import sys
import platform
import json

def get_app_data_dir():
    """Get the application data directory for the current platform."""
    if platform.system() == "Windows":
        return os.path.join(os.environ["APPDATA"], "FrameChanger")
    elif platform.system() == "Darwin":
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "FrameChanger")
    else:
        return os.path.join(os.path.expanduser("~"), ".config", "framechanger")

def get_settings_file():
    """Get the path to the settings file."""
    app_data_dir = get_app_data_dir()
    if not os.path.exists(app_data_dir):
        os.makedirs(app_data_dir)
    return os.path.join(app_data_dir, "settings.json")

def get_database_file():
    """Get the path to the database file."""
    app_data_dir = get_app_data_dir()
    os.makedirs(app_data_dir, exist_ok=True)
    return os.path.join(app_data_dir, "titles.db")

def load_settings():
    """Load settings from the settings file and environment."""
    settings_file = get_settings_file()
    settings = {}
    if os.path.exists(settings_file):
        with open(settings_file, "r") as file:
            try:
                settings = json.load(file)
            except json.JSONDecodeError:
                settings = {}
    env_key = os.getenv("TMDB_API_KEY")
    if env_key:
        settings["api_key"] = env_key
    settings.setdefault("api_key", "")
    return settings

def save_settings(settings):
    """Save settings to the settings file."""
    settings_file = get_settings_file()
    with open(settings_file, 'w') as file:
        json.dump(settings, file)

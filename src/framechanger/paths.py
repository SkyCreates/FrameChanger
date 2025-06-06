from pathlib import Path
import os

# Base directory for app data
APP_DIR = Path(os.getenv("FRAMECHANGER_APP_DIR", Path.home() / ".framechanger"))
APP_DIR.mkdir(parents=True, exist_ok=True)

# Data files stored under APP_DIR
DATABASE_PATH = APP_DIR / "titles.db"
SETTINGS_PATH = APP_DIR / "settings.json"

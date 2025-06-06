# wallpaper_changer.py
# This module handles the wallpaper changing functionality for the FrameChanger app.

import requests
import random
import ctypes
import os
import sqlite3
import json
import platform
import subprocess
from PyQt5.QtWidgets import QApplication, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
import sys
import logging

from .paths import APP_DIR, DATABASE_PATH, SETTINGS_PATH

LOG_FILE = os.path.join(os.path.expanduser("~"), "framechanger.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

API_KEY_ENV_VAR = "TMDB_API_KEY"

image_dir = os.path.join(APP_DIR, 'MovieStillsWallpaperChanger')
settings_file = str(SETTINGS_PATH)

if not os.path.exists(image_dir):
    os.mkdir(image_dir)

def load_settings():
    """Load settings from the settings file and environment."""
    settings = {}
    if os.path.exists(settings_file):
        with open(settings_file, "r") as file:
            try:
                settings = json.load(file)
            except json.JSONDecodeError:
                settings = {}
    env_key = os.getenv(API_KEY_ENV_VAR)
    if env_key:
        settings["api_key"] = env_key
    settings.setdefault("api_key", "")
    return settings

def save_settings(settings):
    """Save settings to the settings file."""
    with open(settings_file, 'w') as file:
        json.dump(settings, file)

def get_api_key():
    """Retrieve the TMDB API key from settings or prompt the user."""
    settings = load_settings()
    api_key = settings.get("api_key", "")
    if not api_key:
        api_key, ok = QInputDialog.getText(None, "TMDB API Key", "Enter your TMDB API Key:")
        if not ok or not api_key:
            QMessageBox.warning(None, "API Key Required", "A TMDB API key is required to fetch wallpapers.")
            return None
        settings["api_key"] = api_key
        save_settings(settings)
    return api_key

def fetch_media_info(title_name, media_type, api_key):
    """Fetch media information from TMDB."""
    media_type = media_type.lower()
    search_url = f'https://api.themoviedb.org/3/search/{media_type}?api_key={api_key}&query={title_name}'
    logging.debug(f'Search URL: {search_url}')
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request Exception: {e}")
        return None

    results = response.json().get('results', [])
    logging.debug(f'Search Results: {results}')
    
    if results:
        best_match = results[0]
        return best_match['id']
    else:
        logging.error(f"No results found for: {title_name} ({media_type})")
        return None

def fetch_backdrop_image(media_id, media_type, api_key):
    """Fetch the backdrop image from TMDB."""
    media_type = media_type.lower()
    images_url = f'https://api.themoviedb.org/3/{media_type}/{media_id}/images?api_key={api_key}'
    logging.debug(f'Images URL: {images_url}')
    
    try:
        response = requests.get(images_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request Exception: {e}")
        return None

    backdrops = [
        img for img in response.json().get('backdrops', [])
        if img['iso_639_1'] is None and round(img['width'] / img['height'], 2) == 1.78
    ]
    logging.debug(f'Backdrops: {backdrops}')
    
    if backdrops:
        backdrop = random.choice(backdrops)
        return f"https://image.tmdb.org/t/p/original{backdrop['file_path']}"
    else:
        logging.error(f"No suitable backdrops found for media ID: {media_id}")
        return None

def save_image(image_url, title_name):
    """Save the image to the local directory."""
    try:
        image_content = requests.get(image_url).content
        with open(os.path.join(image_dir, f'{title_name}.jpg'), 'wb') as f:
            f.write(image_content)
        return os.path.join(image_dir, f'{title_name}.jpg')
    except Exception as e:
        logging.error(f"Error saving image: {e}")
        return None

def download_wallpaper(title_name, media_type, api_key):
    """Download a wallpaper for the given title and return the file path."""
    media_id = fetch_media_info(title_name, media_type, api_key)
    if not media_id:
        logging.error(f"No title found with the name: {title_name}")
        return None
    image_url = fetch_backdrop_image(media_id, media_type, api_key)
    if not image_url:
        logging.error(f"No backdrops found for the title: {title_name}")
        return None
    return save_image(image_url, title_name)

def download_random_image(api_key):
    """Get a random title from the database and download its wallpaper."""
    conn = sqlite3.connect(str(DATABASE_PATH))
    c = conn.cursor()
    c.execute("SELECT * FROM titles")
    rows = c.fetchall()
    if not rows:
        logging.error("No titles found in the database.")
        conn.close()
        return None, ""

    settings = load_settings()
    last_title = settings.get('last_title', "")
    while True:
        title_name, media_type = random.choice(rows)
        if title_name != last_title or len(rows) == 1:
            break

    settings['last_title'] = title_name
    save_settings(settings)
    conn.close()

    image_path = download_wallpaper(title_name, media_type, api_key)
    return image_path, title_name

def set_wallpaper(image_path):
    """Set the wallpaper on the current platform."""
    system = platform.system()
    try:
        if system == "Windows":
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        elif system == "Darwin":
            script = f'''osascript -e 'tell application "System Events" to set picture of every desktop to POSIX file "{image_path}"' '''
            subprocess.run(script, shell=True, check=True)
        elif system == "Linux":
            try:
                subprocess.run([
                    "gsettings",
                    "set",
                    "org.gnome.desktop.background",
                    "picture-uri",
                    f"file://{image_path}",
                ], check=True)
            except Exception:
                subprocess.run(["feh", "--bg-scale", image_path], check=True)
        else:
            logging.error(f"Unsupported OS: {system}")
            return False
        return True
    except Exception as e:
        logging.error(f"Error setting wallpaper: {e}")
        return False

def change_wallpaper(tray_icon):
    """Download a random wallpaper and set it as the background."""
    api_key = get_api_key()
    if not api_key:
        return 1, ""
    image_path, title_name = download_random_image(api_key)
    if not image_path:
        return 1, ""
    if set_wallpaper(image_path):
        return 0, title_name
    logging.error("Failed to set the wallpaper.")
    return 1, ""

def set_specific_wallpaper(title_name, media_type, tray_icon):
    """Set the wallpaper to a specific movie or TV show."""
    api_key = get_api_key()
    if not api_key:
        return 1, ""
    image_path = download_wallpaper(title_name, media_type, api_key)
    if not image_path:
        return 1, ""
    if set_wallpaper(image_path):
        settings = load_settings()
        settings['last_title'] = title_name
        save_settings(settings)
        return 0, title_name
    logging.error("Failed to set the wallpaper.")
    return 1, ""

def initialize_database():
    """Initialize the database with a predefined list of movies and TV shows."""
    titles = [
        ("The Grand Budapest Hotel", "movie"),
        ("The Truman Show", "movie"),
        ("500 Days of Summer", "movie"),
        ("Blade Runner 2049", "movie"),
        ("Inception", "movie"),
        ("Spirited Away", "movie"),
        ("Her", "movie"),
        ("Whiplash", "movie"),
        ("Mad Max Fury Road", "movie"),
        ("Inglourious Basterds", "movie"),
        ("Fargo", "tv"),
        ("True Detective", "tv"),
        ("The Crown", "tv"),
        ("The Handmaid's Tale", "tv"),
        ("Peaky Blinders", "tv"),
        ("Dark", "tv"),
        ("Mindhunter", "tv"),
        ("The Expanse", "tv"),
        ("Better Call Saul", "tv"),
        ("Fleabag", "tv")
    ]

    conn = sqlite3.connect(str(DATABASE_PATH))
    c = conn.cursor()
    
    # Create the titles table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS titles (
            name TEXT NOT NULL,
            media_type TEXT NOT NULL,
            UNIQUE(name, media_type)
        )
    ''')

    # Insert the predefined titles into the table
    c.executemany('''
        INSERT OR IGNORE INTO titles (name, media_type) VALUES (?, ?)
    ''', titles)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    api_key = get_api_key()
    if api_key:
        set_specific_wallpaper("Example Title", "movie", None)

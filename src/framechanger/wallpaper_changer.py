"""
Utility functions for downloading and applying wallpapers.

This module provides functions for downloading wallpapers from TMDB,
saving them locally, and setting them as the desktop background.
"""

import requests
import random
import ctypes
import os
import sqlite3
import platform
import subprocess
from PyQt5.QtWidgets import QApplication, QMessageBox, QInputDialog
import sys
import logging
from .config.config import load_settings, save_settings, get_database_file, get_app_data_dir
from .tmdb_api import fetch_media_info, fetch_backdrop_image

API_KEY_ENV_VAR = "TMDB_API_KEY"

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

def save_image(image_url, title_name):
    """Save the image to the local directory."""
    image_dir = os.path.join(get_app_data_dir(), 'wallpapers')
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
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
    db_file = get_database_file()
    conn = sqlite3.connect(db_file)
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

def change_wallpaper():
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

def set_specific_wallpaper(title_name, media_type):
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

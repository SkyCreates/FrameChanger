import requests
import random
import ctypes
import os
import sqlite3
import json
from PyQt5.QtWidgets import QApplication, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

script_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
image_dir = os.path.join(script_dir, 'MovieStillsWallpaperChanger')
settings_file = os.path.join(script_dir, 'settings.json')

if not os.path.exists(image_dir):
    os.mkdir(image_dir)

def load_settings():
    """Load settings from the settings file."""
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as file:
            return json.load(file)
    else:
        default_settings = {"api_key": ""}
        save_settings(default_settings)
        return default_settings


def save_settings(settings):
    """Save settings to the settings file."""
    with open(settings_file, 'w') as file:
        json.dump(settings, file)

def display_api_key_instructions():
    """Display instructions for obtaining a TMDB API key."""
    instructions = (
        "To use this application, you need a TMDB API key.<br>"
        "Follow these steps to get your API key:<br>"
        "1. Visit: <a href='https://developer.themoviedb.org/reference/intro/getting-started'>TMDB Getting Started</a><br>"
        "2. Click on 'Get an API Key'.<br>"
        "3. Sign in or create a new account.<br>"
        "4. Follow the instructions to generate your API key.<br>"
        "5. Copy the API key and paste it below when prompted."
    )
    msg_box = QMessageBox()
    msg_box.setTextFormat(Qt.RichText)
    msg_box.setWindowTitle("TMDB API Key Instructions")
    msg_box.setText(instructions)
    msg_box.exec_()

def prompt_for_api_key():
    """Prompt the user for their TMDB API key and save it."""
    display_api_key_instructions()
    api_key, ok = QInputDialog.getText(None, "TMDB API Key", "Please enter your TMDB API key:")
    if ok:
        settings = load_settings()
        settings['api_key'] = api_key
        save_settings(settings)
        return api_key
    else:
        QMessageBox.warning(None, "Error", "API key is required to run the application.")
        sys.exit()

def fetch_media_info(title_name, media_type, api_key):
    """Fetch media information from TMDB."""
    media_type = media_type.lower()
    search_url = f'https://api.themoviedb.org/3/search/{media_type}?api_key={api_key}&query={title_name}'
    logging.debug(f'Search URL: {search_url}')
    print(f'Search URL: {search_url}')
    
    response = requests.get(search_url)
    
    if response.status_code == 404:
        logging.error(f"404 Not Found: {search_url}")
        print(f"404 Not Found: {search_url}")
        return None

    response.raise_for_status()
    results = response.json().get('results', [])
    logging.debug(f'Search Results: {results}')
    print(f'Search Results: {results}')
    
    if results:
        best_match = results[0]
        return best_match['id']
    else:
        logging.error(f"No results found for: {title_name} ({media_type})")
        print(f"No results found for: {title_name} ({media_type})")
        return None

def fetch_backdrop_image(media_id, media_type, api_key):
    """Fetch the backdrop image from TMDB."""
    media_type = media_type.lower()
    images_url = f'https://api.themoviedb.org/3/{media_type}/{media_id}/images?api_key={api_key}'
    logging.debug(f'Images URL: {images_url}')
    print(f'Images URL: {images_url}')
    
    response = requests.get(images_url)
    
    if response.status_code == 404:
        logging.error(f"404 Not Found: {images_url}")
        print(f"404 Not Found: {images_url}")
        return None

    response.raise_for_status()
    backdrops = [
        img for img in response.json().get('backdrops', [])
        if img['iso_639_1'] is None and round(img['width'] / img['height'], 2) == 1.78
    ]
    logging.debug(f'Backdrops: {backdrops}')
    print(f'Backdrops: {backdrops}')
    
    if backdrops:
        backdrop = random.choice(backdrops)
        return f"https://image.tmdb.org/t/p/original{backdrop['file_path']}"
    else:
        logging.error(f"No suitable backdrops found for media ID: {media_id}")
        print(f"No suitable backdrops found for media ID: {media_id}")
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
        print(f"Error saving image: {e}")
        return None

def set_wallpaper(image_path):
    """Set the wallpaper to the specified image path."""
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        return True
    except Exception as e:
        logging.error(f"Error setting wallpaper: {e}")
        print(f"Error setting wallpaper: {e}")
        return False

def change_wallpaper(tray_icon):
    """Change the desktop wallpaper to a random image from a movie or TV show in the database."""
    conn = sqlite3.connect('titles.db')
    c = conn.cursor()

    c.execute("SELECT * FROM titles")
    rows = c.fetchall()

    if not rows:
        print("No titles found in the database.")
        return 1, ""

    settings = load_settings()
    last_title = settings.get('last_title', "")

    while True:
        title_name, media_type = random.choice(rows)
        if title_name != last_title or len(rows) == 1:
            break

    settings['last_title'] = title_name
    save_settings(settings)

    conn.close()

    try:
        api_key = settings.get('api_key')
        if not api_key:
            api_key = prompt_for_api_key()

        media_id = fetch_media_info(title_name, media_type, api_key)
        if not media_id:
            print(f"No title found with the name: {title_name}")
            return 1, ""

        image_url = fetch_backdrop_image(media_id, media_type, api_key)
        if not image_url:
            print(f"No backdrops found for the title: {title_name}")
            return 1, ""

        image_path = save_image(image_url, title_name)
        if not image_path:
            print(f"Failed to save the image for the title: {title_name}")
            return 1, ""

        if set_wallpaper(image_path):
            return 0, title_name
        else:
            print("Failed to set the wallpaper.")
            return 1, ""

    except requests.exceptions.RequestException as e:
        logging.error(f"Network Error: {e}")
        print(f"Network Error: {e}")
        return 1, ""
    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")
        return 1, ""


def set_specific_wallpaper(title_name, media_type, tray_icon):
    """Set the wallpaper to a specific movie or TV show."""
    conn = sqlite3.connect('titles.db')
    c = conn.cursor()

    c.execute("SELECT * FROM titles")
    rows = c.fetchall()

    if not rows:
        print("No titles found in the database.")
        return 1, ""

    settings = load_settings()
    settings['last_title'] = title_name
    save_settings(settings)

    conn.close()

    try:
        api_key = settings.get('api_key')
        if not api_key:
            api_key = prompt_for_api_key()

        media_id = fetch_media_info(title_name, media_type, api_key)
        if not media_id:
            print(f"No title found with the name: {title_name}")
            return 1, ""

        image_url = fetch_backdrop_image(media_id, media_type, api_key)
        if not image_url:
            print(f"No backdrops found for the title: {title_name}")
            return 1, ""

        image_path = save_image(image_url, title_name)
        if not image_path:
            print(f"Failed to save the image for the title: {title_name}")
            return 1, ""

        if set_wallpaper(image_path):
            return 0, title_name
        else:
            print("Failed to set the wallpaper.")
            return 1, ""

    except requests.exceptions.RequestException as e:
        logging.error(f"Network Error: {e}")
        print(f"Network Error: {e}")
        return 1, ""
    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")
        return 1, ""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = load_settings()
    api_key = settings.get('api_key')
    if not api_key:
        api_key = prompt_for_api_key()
    set_specific_wallpaper("Example Title", "movie")

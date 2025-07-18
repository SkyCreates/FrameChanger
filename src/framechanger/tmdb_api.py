import requests
import logging
import random

def fetch_media_info(title_name, media_type, api_key):
    """
    Fetch media information from TMDB for a given title and media type.

    :param title_name: The name of the movie or TV show.
    :param media_type: The type of media ('movie' or 'tv').
    :param api_key: The TMDB API key.
    :return: The media ID, or None if not found.
    """
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
    """
    Fetch the backdrop image URL from TMDB for a given media ID.

    :param media_id: The ID of the movie or TV show.
    :param media_type: The type of media ('movie' or 'tv').
    :param api_key: The TMDB API key.
    :return: The backdrop image URL, or None if not found.
    """
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

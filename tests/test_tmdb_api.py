import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from framechanger import tmdb_api
import pytest

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception("API Error")

    def json(self):
        return self.json_data

def mock_get_success(url):
    if "search" in url:
        return MockResponse({"results": [{"id": 123}]}, 200)
    elif "images" in url:
        return MockResponse({"backdrops": [{"file_path": "/test.jpg", "iso_639_1": None, "width": 1920, "height": 1080}]}, 200)
    return MockResponse(None, 404)

def mock_get_failure(url):
    return MockResponse(None, 404)

def test_fetch_media_info_success(monkeypatch):
    monkeypatch.setattr(tmdb_api.requests, "get", mock_get_success)
    media_id = tmdb_api.fetch_media_info("test", "movie", "test_api_key")
    assert media_id == 123

def test_fetch_media_info_failure(monkeypatch):
    monkeypatch.setattr(tmdb_api.requests, "get", mock_get_failure)
    with pytest.raises(Exception):
        tmdb_api.fetch_media_info("test", "movie", "test_api_key")

def test_fetch_backdrop_image_success(monkeypatch):
    monkeypatch.setattr(tmdb_api.requests, "get", mock_get_success)
    image_url = tmdb_api.fetch_backdrop_image(123, "movie", "test_api_key")
    assert image_url == "https://image.tmdb.org/t/p/original/test.jpg"

def test_fetch_backdrop_image_failure(monkeypatch):
    monkeypatch.setattr(tmdb_api.requests, "get", mock_get_failure)
    with pytest.raises(Exception):
        tmdb_api.fetch_backdrop_image(123, "movie", "test_api_key")

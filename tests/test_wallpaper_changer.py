import os
import sqlite3
import sys
import subprocess
import types
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from framechanger import wallpaper_changer as wc


def test_initialize_database(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    wc.initialize_database()
    assert os.path.exists('titles.db')
    conn = sqlite3.connect('titles.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM titles')
    count = c.fetchone()[0]
    conn.close()
    assert count > 0


def test_load_settings(tmp_path, monkeypatch):
    settings_file = tmp_path / 'settings.json'
    monkeypatch.setattr(wc, 'settings_file', str(settings_file))
    settings = wc.load_settings()
    assert 'api_key' in settings


def test_fetch_media_info(monkeypatch):
    called = {}
    def mock_get(url):
        called['url'] = url
        class MockResponse:
            def raise_for_status(self):
                pass
            def json(self):
                return {'results': [{'id': 42}]}
        return MockResponse()
    monkeypatch.setattr(wc.requests, 'get', mock_get)
    media_id = wc.fetch_media_info('The Matrix', 'movie', 'KEY')
    assert media_id == 42
    assert 'search/movie' in called['url']


def test_fetch_backdrop_image(monkeypatch):
    def mock_get(url):
        class MockResponse:
            def raise_for_status(self):
                pass
            def json(self):
                return {
                    'backdrops': [
                        {'file_path': '/img.jpg', 'iso_639_1': None, 'width': 1920, 'height': 1080}
                    ]
                }
        return MockResponse()
    monkeypatch.setattr(wc.requests, 'get', mock_get)
    url = wc.fetch_backdrop_image(1, 'movie', 'KEY')
    assert url == 'https://image.tmdb.org/t/p/original/img.jpg'


def test_set_wallpaper(monkeypatch):
    path = '/tmp/test img.jpg'
    called = {}
    # Windows
    def win_call(action, param, image_path, flags):
        called["windows"] = image_path
        return True
    monkeypatch.setattr(wc.platform, "system", lambda: "Windows")
    win_dll = types.SimpleNamespace(user32=types.SimpleNamespace(SystemParametersInfoW=win_call))
    monkeypatch.setattr(wc.ctypes, "windll", win_dll, raising=False)
    assert wc.set_wallpaper(path) is True
    assert called['windows'] == path

    # macOS
    monkeypatch.setattr(wc.platform, 'system', lambda: 'Darwin')
    def mac_run(cmd, shell, check):
        called['darwin'] = cmd
        return subprocess.CompletedProcess(cmd, 0)
    monkeypatch.setattr(wc.subprocess, 'run', mac_run)
    assert wc.set_wallpaper(path) is True
    assert path in called['darwin']

    # Linux
    monkeypatch.setattr(wc.platform, 'system', lambda: 'Linux')
    def linux_run(cmd, check):
        called['linux'] = cmd
        return subprocess.CompletedProcess(cmd, 0)
    monkeypatch.setattr(wc.subprocess, 'run', linux_run)
    assert wc.set_wallpaper(path) is True
    assert called['linux'][4] == f'file://{path}'


def test_cross_platform_paths(monkeypatch):
    """Ensure set_wallpaper handles different path styles."""
    win_path = r'C:\\User\\wallpaper.jpg'
    lin_path = '/home/user/wallpaper.jpg'
    win_dll = types.SimpleNamespace(user32=types.SimpleNamespace(SystemParametersInfoW=lambda *a: True))
    monkeypatch.setattr(wc.ctypes, "windll", win_dll, raising=False)
    monkeypatch.setattr(wc.subprocess, 'run', lambda *a, **k: subprocess.CompletedProcess(a, 0))

    monkeypatch.setattr(wc.platform, 'system', lambda: 'Windows')
    assert wc.set_wallpaper(win_path)

    monkeypatch.setattr(wc.platform, 'system', lambda: 'Linux')
    assert wc.set_wallpaper(lin_path)

import os
import sqlite3
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from framechanger import wallpaper_changer as wc
from framechanger import paths


def test_initialize_database(tmp_path, monkeypatch):
    monkeypatch.setattr(paths, 'APP_DIR', tmp_path, raising=False)
    monkeypatch.setattr(paths, 'DATABASE_PATH', tmp_path / 'titles.db', raising=False)
    monkeypatch.setattr(wc, 'APP_DIR', tmp_path, raising=False)
    monkeypatch.setattr(wc, 'DATABASE_PATH', tmp_path / 'titles.db', raising=False)
    wc.initialize_database()
    assert (tmp_path / 'titles.db').exists()
    conn = sqlite3.connect(tmp_path / 'titles.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM titles')
    count = c.fetchone()[0]
    conn.close()
    assert count > 0


def test_load_settings(tmp_path, monkeypatch):
    monkeypatch.setattr(paths, 'APP_DIR', tmp_path, raising=False)
    monkeypatch.setattr(paths, 'SETTINGS_PATH', tmp_path / 'settings.json', raising=False)
    monkeypatch.setattr(wc, 'APP_DIR', tmp_path, raising=False)
    monkeypatch.setattr(wc, 'settings_file', str(tmp_path / 'settings.json'), raising=False)
    settings = wc.load_settings()
    assert 'api_key' in settings

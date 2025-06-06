import os
import sqlite3
import sys
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

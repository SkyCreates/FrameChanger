import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from framechanger.config import config

def test_get_app_data_dir(monkeypatch):
    # Test for Windows
    monkeypatch.setattr(config.platform, "system", lambda: "Windows")
    monkeypatch.setenv("APPDATA", "/tmp")
    assert config.get_app_data_dir() == "/tmp/FrameChanger"

    # Test for macOS
    monkeypatch.setattr(config.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(os.path, "expanduser", lambda path: "/tmp")
    assert config.get_app_data_dir() == "/tmp/Library/Application Support/FrameChanger"

    # Test for Linux
    monkeypatch.setattr(config.platform, "system", lambda: "Linux")
    monkeypatch.setattr(os.path, "expanduser", lambda path: "/tmp")
    assert config.get_app_data_dir() == "/tmp/.config/framechanger"

def test_get_settings_file(monkeypatch):
    monkeypatch.setattr(config, "get_app_data_dir", lambda: "/tmp/framechanger")
    assert config.get_settings_file() == "/tmp/framechanger/settings.json"

def test_get_database_file(monkeypatch):
    monkeypatch.setattr(config, "get_app_data_dir", lambda: "/tmp/framechanger")
    assert config.get_database_file() == "/tmp/framechanger/titles.db"

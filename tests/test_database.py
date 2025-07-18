import os
import sqlite3
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from framechanger import database
from framechanger.config import config

def test_initialize_database(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "get_app_data_dir", lambda: str(tmp_path))
    database.initialize_database()
    db_path = os.path.join(tmp_path, "titles.db")
    assert os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM titles')
    count = c.fetchone()[0]
    conn.close()
    assert count > 0

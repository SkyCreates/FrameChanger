import sqlite3
import os
from .config.config import get_database_file

def initialize_database():
    """
    Initialize the database by creating the 'titles' table if it doesn't
    exist and populating it with a predefined list of movies and TV shows.
    """
    db_file = get_database_file()
    conn = sqlite3.connect(db_file)
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
    c.executemany('''
        INSERT OR IGNORE INTO titles (name, media_type) VALUES (?, ?)
    ''', titles)

    conn.commit()
    conn.close()

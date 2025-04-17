import sqlite3
from config import db_config

def get_db_connection():
    """Create and return a connection to the SQLite database"""
    conn = sqlite3.connect(db_config.DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn
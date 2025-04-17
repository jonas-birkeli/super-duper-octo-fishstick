import sqlite3

def get_db_connection():
    """Create and return a connection to the SQLite database"""
    conn = sqlite3.connect('fitness_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn
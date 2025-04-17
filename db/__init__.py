from .connection import get_db_connection
from .schema import create_tables

def init_db():
    """Initialize the database with content i fnot exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    create_tables(cursor)
    conn.commit()
    conn.close()
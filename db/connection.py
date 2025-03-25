import mysql.connector
import streamlit as st
from config.db_config import USE_MYSQL, MYSQL_CONFIG



class DatabaseConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**MYSQL_CONFIG)
            self.cursor = self.conn.cursor(buffered=True)
            st.sidebar.success('Connected to NTNU MySQL database!')
            return True
        except mysql.connector.Error as err:
            st.sidebar.error(f'Error connecting to MySQL database: {err}')
            return False

    def execute_query(self, query, params=None, commit=False):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            if commit:
                self.conn.commit()

            return self.cursor
        except Exception as e:
            st.error(f'Database error: {e}')

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def last_insert_id(self):
        return self.cursor.lastrowid

    def close(self):
        if self.conn:
            self.conn.close()

def get_connection() -> DatabaseConnection:
    if 'db_connection' not in st.session_state:
        st.session_state.db_connection = DatabaseConnection
        st.session_state.db_connection.connect()

    return st.session_state.db_connection
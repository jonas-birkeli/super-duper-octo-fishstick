import pandas as pd
from db.connection import get_db_connection

def get_all_users():
    """Get all users from the database"""
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM Users", conn)
    conn.close()
    return df

def get_user_by_id(user_id):
    """Get a specific user by ID"""
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM Users WHERE userID = ?", conn, params=(user_id,))
    conn.close()
    return df

def add_user(fname, lname, weight, dob, sex):
    """Add a new user to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Users (fName, lName, weight, DOB, sex) VALUES (?, ?, ?, ?, ?)",
            (fname, lname, weight, dob, sex)
        )
        conn.commit()
        result = {"success": True, "user_id": cursor.lastrowid}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result

def update_user(user_id, fname, lname, weight, dob, sex):
    """Update an existing user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Users SET fName=?, lName=?, weight=?, DOB=?, sex=? WHERE userID=?",
            (fname, lname, weight, dob, sex, user_id)
        )
        conn.commit()
        result = {"success": True, "rows_affected": cursor.rowcount}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result

def delete_user(user_id):
    """Delete a user from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Users WHERE userID=?", (user_id,))
        conn.commit()
        result = {"success": True, "rows_affected": cursor.rowcount}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result

def get_user_ids():
    """Get all user IDs for dropdowns"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT userID FROM Users")
    user_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return user_ids
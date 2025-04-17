import pandas as pd
from db.connection import get_db_connection

def get_all_health_records():
    """Get all health records"""
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM Health", conn)
    conn.close()
    return df

def get_health_by_user(user_id):
    """Get health records for a specific user"""
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM Health WHERE userID = ? ORDER BY date DESC",
                    conn, params=(user_id,))
    conn.close()
    return df

def add_health_record(user_id, date, heartrate, vo2max, hr_variation, sleeptime):
    """Add a new health record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Health (userID, date, heartrate, VO2max, "
            "HRvariation, sleeptime) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, date, heartrate, vo2max, hr_variation, sleeptime)
        )
        conn.commit()
        result = {"success": True}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result

def update_health_record(user_id, date, heartrate, vo2max, hr_variation, sleeptime):
    """Update an existing health record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Health SET heartrate=?, VO2max=?, HRvariation=?, "
            "sleeptime=? WHERE userID=? AND date=?",
            (heartrate, vo2max, hr_variation, sleeptime, user_id, date)
        )
        conn.commit()
        result = {"success": True, "rows_affected": cursor.rowcount}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result

def delete_health_record(user_id, date):
    """Delete a health record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Health WHERE userID=? AND date=?", (user_id, date))
        conn.commit()
        result = {"success": True, "rows_affected": cursor.rowcount}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result
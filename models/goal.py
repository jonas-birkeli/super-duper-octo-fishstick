import pandas as pd
from db.connection import get_db_connection

def get_all_goals():
    """Get all goals"""
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM Goals", conn)
    conn.close()
    return df

def get_goals_by_user(user_id):
    """Get goals for a specific user"""
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM Goals WHERE userID = ?",
                    conn, params=(user_id,))
    conn.close()
    return df

def add_goal(user_id, goal_name, amount, metric, completed):
    """Add a new goal"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Goals (userID, goalName, amount, metric, completed) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, goal_name, amount, metric, completed)
        )
        conn.commit()
        result = {"success": True}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result

def update_goal(user_id, goal_name, amount, metric, completed):
    """Update an existing goal"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Goals SET amount=?, metric=?, completed=? WHERE userID=? "
            "AND goalName=?",
            (amount, metric, completed, user_id, goal_name)
        )
        conn.commit()
        result = {"success": True, "rows_affected": cursor.rowcount}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result

def delete_goal(user_id, goal_name):
    """Delete a goal"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Goals WHERE userID=? AND goalName=?", (user_id, goal_name))
        conn.commit()
        result = {"success": True, "rows_affected": cursor.rowcount}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result
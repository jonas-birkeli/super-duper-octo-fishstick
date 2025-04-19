import pandas as pd
from db.connection import get_db_connection

def get_all_goals():
    """Retrieve all goals"""
    conn = get_db_connection()
    df = pd.read_sql("""
    SELECT g.*, u.fName || ' ' || u.lName AS userName 
    FROM Goals g
    JOIN Users u ON g.userID = u.userID
    ORDER BY g.userID, g.goalName
    """, conn)
    conn.close()
    return df

def get_goals_by_user(user_id):
    """Retrieve goals for a specific user"""
    conn = get_db_connection()
    df = pd.read_sql("""
    SELECT * FROM Goals 
    WHERE userID = ? 
    ORDER BY goalName
    """, conn, params=(user_id,))
    conn.close()
    return df

def add_goal(user_id, goal_name, amount, metric, completed=0):
    """Add a new goal"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Goals (userID, goalName, amount, metric, completed) VALUES (?, ?, ?, ?, ?)",
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
            "UPDATE Goals SET amount=?, metric=?, completed=? WHERE userID=? AND goalName=?",
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

def get_common_goal_names():
    """Get a list of common fitness goal names"""
    return [
        "Run Distance",
        "Daily Steps",
        "Weight Loss",
        "Muscle Gain",
        "Exercise Time",
        "Calorie Burn",
        "Lift Weights",
        "Improve Cardio",
        "Lower Body Fat",
        "Increase Strength",
        "Improve Flexibility"
    ]

def get_common_metrics():
    """Get a list of common fitness metrics"""
    return [
        "kg", "lbs", "km", "mi", "steps", "min", "hrs", "cal", "%", "reps", "sessions"
    ]
import pandas as pd
from db.connection import get_db_connection

def get_all_exercises():
    """Retrieve all exercises from the database"""
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM Exercise ORDER BY name", conn)
    conn.close()
    return df

def add_exercise(name, muscle_group):
    """Add a new exercise to the database, format name (muscleGroup)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Exercise (name, muscleGroup) VALUES (?, ?)",
            (name, muscle_group)
        )
        conn.commit()
        result = {"success": True, "exercise_id": cursor.lastrowid}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result

def update_exercise(exercise_id, name, muscle_group):
    """Update an existing exercise"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Exercise SET name=?, muscleGroup=? WHERE exerciseID=?",
            (name, muscle_group, exercise_id)
        )
        conn.commit()
        result = {"success": True, "rows_affected": cursor.rowcount}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result

def delete_exercise(exercise_id):
    """Delete an exercise from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # First check if the exercise is used in any workouts
        cursor.execute("SELECT COUNT(*) FROM Weightlift WHERE exerciseID=?", (exercise_id,))
        count = cursor.fetchone()[0]
        if count > 0:
            result = {"success": False, "error": f"Cannot delete exercise that is used in {count} workout sets. Remove those workout records first."}
        else:
            cursor.execute("DELETE FROM Exercise WHERE exerciseID=?", (exercise_id,))
            conn.commit()
            result = {"success": True, "rows_affected": cursor.rowcount}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result

def get_exercise_by_id(exercise_id):
    """Get an exercise by ID"""
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM Exercise WHERE exerciseID = ?", conn, params=(exercise_id,))
    conn.close()
    return df
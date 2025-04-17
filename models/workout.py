import pandas as pd
from db.connection import get_db_connection

def get_all_workouts():
    """Retrieve all workouts"""
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM Workout ORDER BY startTime DESC", conn)
    conn.close()
    return df

def get_workouts_by_user(user_id):
    """Retrieve workouts for a specific user"""
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM Workout WHERE userID = ? ORDER BY startTime DESC",
                    conn, params=(user_id,))
    conn.close()
    return df

def add_workout(user_id, start_time, end_time, max_hr, workout_type):
    """Add a new workout"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Workout (userID, startTime, endTime, maxHR, workoutType) VALUES (?, ?, ?, ?, ?)",
            (user_id, start_time, end_time, max_hr, workout_type)
        )
        conn.commit()
        result = {"success": True, "workout_id": cursor.lastrowid}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result

def update_workout(workout_id, user_id, start_time, end_time, max_hr, workout_type):
    """Update an existing workout"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Workout SET userID=?, startTime=?, endTime=?, maxHR=?, workoutType=? WHERE workoutID=?",
            (user_id, start_time, end_time, max_hr, workout_type, workout_id)
        )
        conn.commit()
        result = {"success": True, "rows_affected": cursor.rowcount}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result

def delete_workout(workout_id):
    """Delete a workout"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Workout WHERE workoutID=?", (workout_id,))
        conn.commit()
        result = {"success": True, "rows_affected": cursor.rowcount}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result

def get_workout_ids():
    """Get all workout IDs for dropdowns"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT workoutID FROM Workout")
    workout_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return workout_ids

def get_workout_statistics():
    """Get workout statistics for visualization"""
    conn = get_db_connection()
    query = """
    SELECT 
        u.userID,
        u.fName || ' ' || u.lName AS userName,
        w.workoutType,
        AVG(JULIANDAY(w.endTime) - JULIANDAY(w.startTime)) * 24 * 60 AS avgDurationMinutes
    FROM 
        Users u
    JOIN 
        Workout w ON u.userID = w.userID
    GROUP BY 
        u.userID, w.workoutType
    ORDER BY 
        u.userID, w.workoutType
    """
    try:
        df = pd.read_sql(query, conn)
        result = {"success": True, "data": df}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result


def add_run_interval(workout_id, interval_nr, distance, pace, incline):
    """Add a new running interval to a run workout"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check the columns in the Run table
        cursor.execute("PRAGMA table_info(Run)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        # Use the correct column name based on what's in the database
        interval_column = "intervalNr" if "intervalNr" in column_names else "intervalNr"
        if "intervalNR" in column_names:
            interval_column = "intervalNR"

        # Create the SQL query dynamically based on the actual column name
        query = f"INSERT INTO Run (workoutID, {interval_column}, distance, pace, incline) VALUES (?, ?, ?, ?, ?)"

        cursor.execute(query,
                       (workout_id, interval_nr, distance, pace, incline))
        conn.commit()
        result = {"success": True}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result

def add_weightlift_set(workout_id, exercise_id, set_nr, reps, weight):
    """Add a new weightlifting set to a weightlift workout"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Weightlift (workoutID, exerciseID, setNr, reps, weight) VALUES (?, ?, ?, ?, ?)",
            (workout_id, exercise_id, set_nr, reps, weight)
        )
        conn.commit()
        result = {"success": True}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result


def get_exercises():
    """Get all exercises for dropdowns"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if the Exercise table exists and has the correct structure
        cursor.execute("PRAGMA table_info(Exercise)")
        columns = cursor.fetchall()
        column_names = [col[1].lower() for col in columns]

        # If the table structure is correct
        if 'name' in column_names and 'musclegroup' in column_names:
            # Find the actual column names (respecting case)
            name_col = next(
                (col[1] for col in columns if col[1].lower() == 'name'), None)
            muscle_col = next(
                (col[1] for col in columns if col[1].lower() == 'musclegroup'),
                None)

            # Build the query using the actual column names
            query = f"SELECT exerciseID, {name_col}, {muscle_col} FROM Exercise"
            cursor.execute(query)
            exercises = cursor.fetchall()

            result = {"success": True, "exercises": [
                {"id": ex[0], "name": ex[1], "muscleGroup": ex[2]}
                for ex in exercises
            ]}
        else:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Exercise (
              exerciseID INTEGER PRIMARY KEY AUTOINCREMENT,
              name VARCHAR(32) NOT NULL,
              muscleGroup VARCHAR(32)
            )
            """)

            cursor.execute("SELECT COUNT(*) FROM Exercise")
            count = cursor.fetchone()[0]

            if count == 0:
                sample_exercises = [
                    ('Bench Press', 'Chest'),
                    ('Squat', 'Legs'),
                    ('Deadlift', 'Back'),
                    ('Shoulder Press', 'Shoulders'),
                    ('Bicep Curl', 'Arms')
                ]
                cursor.executemany(
                    "INSERT INTO Exercise (name, muscleGroup) VALUES (?, ?)",
                    sample_exercises
                )
                conn.commit()

                cursor.execute(
                    "SELECT exerciseID, name, muscleGroup FROM Exercise")
                exercises = cursor.fetchall()
                result = {"success": True, "exercises": [
                    {"id": ex[0], "name": ex[1], "muscleGroup": ex[2]}
                    for ex in exercises
                ]}
            else:
                cursor.execute(
                    "SELECT exerciseID, name, muscleGroup FROM Exercise")
                exercises = cursor.fetchall()
                result = {"success": True, "exercises": [
                    {"id": ex[0], "name": ex[1], "muscleGroup": ex[2]}
                    for ex in exercises
                ]}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result
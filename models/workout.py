import pandas as pd
from db.connection import get_connection


class WorkoutModel:
    @staticmethod
    def get_all_workouts():
        db = get_connection()
        db.execute_query("""
            SELECT w.workoutID, u.fName || ' ' || u.lName as user, w.starttime, w.endtime, 
                   w.workoutType, CASE WHEN w.workoutType = 'Run' THEN r.distance ELSE NULL END as distance
            FROM Workout w
            JOIN Users u ON w.userID = u.userID
            LEFT JOIN Run r ON w.workoutID = r.workoutID
            ORDER BY w.starttime DESC
        """)
        workouts = db.fetchall()

        if workouts:
            return pd.DataFrame(workouts,
                                columns=["ID", "User", "Start Time", "End Time",
                                         "Type", "Distance (km)"])
        return pd.DataFrame()

    @staticmethod
    def get_user_workouts(user_id, limit=5):
        db = get_connection()
        db.execute_query("""
            SELECT w.workoutID, w.starttime, w.workoutType, 
                   CASE WHEN w.workoutType = 'Run' THEN r.distance ELSE NULL END as distance
            FROM Workout w
            LEFT JOIN Run r ON w.workoutID = r.workoutID
            WHERE w.userID = ?
            ORDER BY w.starttime DESC
            LIMIT ?
        """, (user_id, limit))
        return db.fetchall()

    @staticmethod
    def add_workout(user_id, workout_type, start_time, end_time, max_hr,
        **kwargs):
        db = get_connection()
        try:
            # Insert into Workout table
            db.execute_query(
                "INSERT INTO Workout (userID, starttime, endtime, maxHR, workoutType) VALUES (?, ?, ?, ?, ?)",
                (user_id, start_time, end_time, max_hr, workout_type),
                commit=True
            )
            workout_id = db.last_insert_id()

            # Insert into Run or Weightlift table based on workout type
            if workout_type == "Run":
                distance = kwargs.get('distance', 0)
                avg_pace = kwargs.get('avg_pace', 0)

                db.execute_query(
                    "INSERT INTO Run (workoutID, distance, avgPace) VALUES (?, ?, ?)",
                    (workout_id, distance, avg_pace),
                    commit=True
                )
            else:  # Weightlift
                active_minutes = kwargs.get('active_minutes', 0)
                rest_minutes = kwargs.get('rest_minutes', 0)

                db.execute_query(
                    "INSERT INTO Weightlift (workoutID, activeMinutes, restMinutes) VALUES (?, ?, ?)",
                    (workout_id, active_minutes, rest_minutes),
                    commit=True
                )

            return True, "Workout added successfully!"
        except Exception as e:
            return False, f"Error adding workout: {e}"

    @staticmethod
    def delete_workout(workout_id):
        db = get_connection()
        try:
            # Get workout type
            db.execute_query(
                "SELECT workoutType FROM Workout WHERE workoutID = ?",
                (workout_id,))
            workout_type = db.fetchone()[0]

            # Delete from the specific type table first
            if workout_type == "Run":
                db.execute_query("DELETE FROM Run WHERE workoutID = ?",
                                 (workout_id,), commit=True)
            else:  # Weightlift
                db.execute_query("DELETE FROM Weightlift WHERE workoutID = ?",
                                 (workout_id,), commit=True)

            # Then delete from the main Workout table
            db.execute_query("DELETE FROM Workout WHERE workoutID = ?",
                             (workout_id,), commit=True)

            return True, "Workout deleted successfully!"
        except Exception as e:
            return False, f"Error deleting workout: {e}"

    @staticmethod
    def get_workout_stats():
        db = get_connection()
        db.execute_query("""
            SELECT workoutType, 
                   AVG(strftime('%s', endtime) - strftime('%s', starttime))/60 as avg_duration_minutes
            FROM Workout
            GROUP BY workoutType
        """)
        return db.fetchall()

    @staticmethod
    def get_user_activity_summary():
        db = get_connection()
        db.execute_query("""
            SELECT u.userID, u.fName || ' ' || u.lName as user, 
                   COUNT(w.workoutID) as total_workouts,
                   COUNT(CASE WHEN w.workoutType = 'Run' THEN 1 END) as run_workouts,
                   COUNT(CASE WHEN w.workoutType = 'Weightlift' THEN 1 END) as weightlift_workouts
            FROM Users u
            LEFT JOIN Workout w ON u.userID = w.userID
            GROUP BY u.userID
        """)
        return db.fetchall()


class ExerciseModel:

    @staticmethod
    def get_all_exercise_types():
        db = get_connection()
        db.execute_query(
            "SELECT exerciseID, name, musclegroup FROM ExerciseType")
        return db.fetchall()

    @staticmethod
    def add_exercise_to_workout(workout_id, exercise_id, set_nr, reps, weight):
        """Add an exercise to a weightlifting workout."""
        db = get_connection()
        try:
            db.execute_query(
                "INSERT INTO Exercise (workoutID, exerciseID, setNr, reps, weight) VALUES (?, ?, ?, ?, ?)",
                (workout_id, exercise_id, set_nr, reps, weight),
                commit=True
            )
            return True, "Exercise added successfully!"
        except Exception as e:
            return False, f"Error adding exercise: {e}"
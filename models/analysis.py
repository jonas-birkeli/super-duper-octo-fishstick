import pandas as pd
from db.connection import get_db_connection

def get_user_progress_overview():
    """Get data from the UserProgressOverview view"""
    conn = get_db_connection()
    try:
        df = pd.read_sql("SELECT * FROM UserProgressOverview", conn)
        result = {"success": True, "data": df}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result


def get_exercise_effectiveness_analysis():
    """Get data from the ExerciseEffectivenessAnalysis view"""
    conn = get_db_connection()
    try:
        # Use the view directly instead of executing a query
        df = pd.read_sql("SELECT * FROM ExerciseEffectivenessAnalysis", conn)
        result = {"success": True, "data": df}
    except Exception as e:
        result = {"success": False, "error": str(e)}
    finally:
        conn.close()
    return result
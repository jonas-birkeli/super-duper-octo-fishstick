"""
Health model operations for the fitness tracking application.
Handles CRUD operations for health metrics data.
"""

import pandas as pd
from db.connection import get_connection


class HealthModel:
    @staticmethod
    def get_user_health_records(user_id):
        db = get_connection()
        db.execute_query("""
            SELECT date, heartrate, VO2max, HRvariation, sleeptime, sleepQuality
            FROM Health
            WHERE userID = ?
            ORDER BY date DESC
        """, (user_id,))
        records = db.fetchall()

        if records:
            return pd.DataFrame(records,
                                columns=["Date", "Heart Rate", "VO2max",
                                         "HR Variation", "Sleep Time",
                                         "Sleep Quality"])
        return pd.DataFrame()

    @staticmethod
    def add_health_record(user_id, record_date, heart_rate, vo2max,
        hr_variation, sleep_time, sleep_quality):
        db = get_connection()
        try:
            db.execute_query(
                """INSERT INTO Health 
                   (userID, date, heartrate, VO2max, HRvariation, sleeptime, sleepQuality) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (user_id, record_date, heart_rate, vo2max, hr_variation,
                 sleep_time, sleep_quality),
                commit=True
            )
            return True, "Health record added successfully!"
        except Exception as e:
            return False, f"Error adding health record: {e}"

    @staticmethod
    def update_health_record(user_id, record_date, heart_rate, vo2max,
        hr_variation, sleep_time, sleep_quality):
        db = get_connection()
        try:
            db.execute_query(
                """UPDATE Health 
                   SET heartrate = ?, VO2max = ?, HRvariation = ?, sleeptime = ?, sleepQuality = ? 
                   WHERE userID = ? AND date = ?""",
                (heart_rate, vo2max, hr_variation, sleep_time, sleep_quality,
                 user_id, record_date),
                commit=True
            )
            return True, "Health record updated successfully!"
        except Exception as e:
            return False, f"Error updating health record: {e}"

    @staticmethod
    def delete_health_record(user_id, record_date):
        db = get_connection()
        try:
            db.execute_query(
                "DELETE FROM Health WHERE userID = ? AND date = ?",
                (user_id, record_date),
                commit=True
            )
            return True, "Health record deleted successfully!"
        except Exception as e:
            return False, f"Error deleting health record: {e}"

    @staticmethod
    def get_health_trend_data(user_id, metric):
        db = get_connection()

        # Map metric name to column name
        column_mapping = {
            "Heart Rate": "heartrate",
            "VO2max": "VO2max",
            "HR Variation": "HRvariation",
            "Sleep Time": "sleeptime",
            "Sleep Quality": "sleepQuality"
        }

        column = column_mapping.get(metric)
        if not column:
            return [], []

        db.execute_query(f"""
            SELECT date, {column}
            FROM Health
            WHERE userID = ?
            ORDER BY date ASC
        """, (user_id,))

        records = db.fetchall()
        if not records:
            return [], []

        dates = [record[0] for record in records]
        values = [record[1] for record in records]

        return dates, values
import pandas as pd
from db.connection import get_connection


class GoalModel:
    @staticmethod
    def get_all_goals():
        db = get_connection()
        db.execute_query("""
            SELECT g.userID, u.fName || ' ' || u.lName as user, g.goalName, g.amount, g.metric, g.completed
            FROM Goals g
            JOIN Users u ON g.userID = u.userID
            ORDER BY u.userID, g.goalName
        """)
        goals = db.fetchall()

        if goals:
            return pd.DataFrame(goals,
                                columns=["User ID", "User", "Goal", "Amount",
                                         "Metric", "Completed"])
        return pd.DataFrame()

    @staticmethod
    def get_user_goals(user_id):
        db = get_connection()
        db.execute_query(
            "SELECT goalName, amount, metric, completed FROM Goals WHERE userID = ?",
            (user_id,)
        )
        return db.fetchall()


    @staticmethod
    def add_goal(user_id, goal_name, amount, metric, completed=False):
        db = get_connection()
        try:
            db.execute_query(
                "INSERT INTO Goals (userID, goalName, amount, metric, completed) VALUES (?, ?, ?, ?, ?)",
                (user_id, goal_name, amount, metric, completed),
                commit=True
            )
            return True, "Goal added successfully!"
        except Exception as e:
            return False, f"Error adding goal: {e}"

    @staticmethod
    def update_goal(user_id, goal_name, amount=None, metric=None,
        completed=None):
        """Update an existing goal."""
        db = get_connection()
        try:
            # First check if the goal exists
            db.execute_query(
                "SELECT * FROM Goals WHERE userID = ? AND goalName = ?",
                (user_id, goal_name)
            )
            goal = db.fetchone()
            if not goal:
                return False, f"Goal '{goal_name}' not found for this user."

            # Build update query based on provided parameters
            query_parts = []
            params = []

            if amount is not None:
                query_parts.append("amount = ?")
                params.append(amount)

            if metric is not None:
                query_parts.append("metric = ?")
                params.append(metric)

            if completed is not None:
                query_parts.append("completed = ?")
                params.append(completed)

            if not query_parts:
                return True, "No changes to update."

            query = f"UPDATE Goals SET {', '.join(query_parts)} WHERE userID = ? AND goalName = ?"
            params.extend([user_id, goal_name])

            db.execute_query(query, params, commit=True)
            return True, "Goal updated successfully!"
        except Exception as e:
            return False, f"Error updating goal: {e}"

    @staticmethod
    def mark_goal_completed(user_id, goal_name):
        return GoalModel.update_goal(user_id, goal_name, completed=True)

    @staticmethod
    def delete_goal(user_id, goal_name):
        db = get_connection()
        try:
            db.execute_query(
                "DELETE FROM Goals WHERE userID = ? AND goalName = ?",
                (user_id, goal_name),
                commit=True
            )
            return True, "Goal deleted successfully!"
        except Exception as e:
            return False, f"Error deleting goal: {e}"
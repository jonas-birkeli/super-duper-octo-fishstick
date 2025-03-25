import pandas as pd
from db.connection import get_connection


class UserModel:
    @staticmethod
    def get_all_users():
        db = get_connection()
        db.execute_query("SELECT * FROM Users")
        users = db.fetchall()

        if users:
            return pd.DataFrame(users,
                                columns=["User ID", "First Name", "Last Name",
                                         "Weight (kg)", "DOB", "Sex"])
        return pd.DataFrame()

    @staticmethod
    def get_users_for_dropdown():
        db = get_connection()
        db.execute_query(
            "SELECT userID, fName || ' ' || lName AS fullName FROM Users")
        return {user[0]: user[1] for user in db.fetchall()}

    @staticmethod
    def get_user_by_id(user_id):
        db = get_connection()
        db.execute_query("SELECT * FROM Users WHERE userID = ?", (user_id,))
        return db.fetchone()

    @staticmethod
    def add_user(fname, lname, weight, dob, sex):
        db = get_connection()
        try:
            db.execute_query(
                "INSERT INTO Users (fName, lName, weight, DOB, sex) VALUES (?, ?, ?, ?, ?)",
                (fname, lname, weight, dob, sex),
                commit=True
            )
            return True, "User added successfully!"
        except Exception as e:
            return False, f"Error adding user: {e}"

    @staticmethod
    def update_user(user_id, fname, lname, weight, dob, sex):
        db = get_connection()
        try:
            db.execute_query(
                "UPDATE Users SET fName = ?, lName = ?, weight = ?, DOB = ?, sex = ? WHERE userID = ?",
                (fname, lname, weight, dob, sex, user_id),
                commit=True
            )
            return True, "User updated successfully!"
        except Exception as e:
            return False, f"Error updating user: {e}"

    @staticmethod
    def delete_user(user_id):
        db = get_connection()
        try:
            db.execute_query("DELETE FROM Users WHERE userID = ?", (user_id,),
                             commit=True)
            return True, "User deleted successfully!"
        except Exception as e:
            return False, f"Error deleting user: {e}"
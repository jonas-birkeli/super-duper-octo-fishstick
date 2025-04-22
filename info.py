import streamlit as st
from db import init_db

init_db()

st.title("Fitness Tracker Database App")

st.subheader("About this application")
st.write("""
Things you can do:
- Manage users (add, update, delete)
- Record health metrics
- Track workouts
- Manage goals
- Compare users to users

By:
Benjamin, Johan, Jonas, Sofiya and Torbjørn
""")

st.subheader("Database content simplified")

with st.expander("View Database Statistics"):
    import sqlite3

    conn = sqlite3.connect('fitness_tracker.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Users")
    user_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Health")
    health_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Workout")
    workout_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Goals")
    goal_count = cursor.fetchone()[0]

    conn.close()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Users", user_count)
    col2.metric("Health Records", health_count)
    col3.metric("Workouts", workout_count)
    col4.metric("Goals", goal_count)
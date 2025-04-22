import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from models.user import get_user_ids
from models.workout import (
    get_all_workouts,
    add_workout,
    delete_workout,
    add_run_interval,
    add_weightlift_set,
    get_exercises
)


def workouts_page():
    """Workout management page - CRUD operations for workouts"""
    st.header("Workouts")

    # Read operation - display all workouts
    workouts_df = get_all_workouts()

    # Format datetime columns for better display
    if not workouts_df.empty and 'startTime' in workouts_df.columns and 'endTime' in workouts_df.columns:
        try:
            workouts_df['startTime'] = pd.to_datetime(
                workouts_df['startTime']).dt.strftime('%Y-%m-%d %H:%M')
            workouts_df['endTime'] = pd.to_datetime(
                workouts_df['endTime']).dt.strftime('%Y-%m-%d %H:%M')
        except Exception:
            pass

    st.write("Current Workouts:")
    st.dataframe(workouts_df)

    st.subheader("Add New Workout")

    user_ids = get_user_ids()

    if not user_ids:
        st.warning("No users found. Please add a user first.")
        return

    # Use tabs to separate different workout types
    tab1, tab2 = st.tabs(["Running Workout", "Weightlifting Workout"])

    # Tab 1: Running Workout
    with tab1:
        with st.form("add_run_workout_form"):
            st.write("Create a new running workout")
            user_id = st.selectbox("User", user_ids, key="run_user")

            # Date and time selection
            workout_date = st.date_input("Workout Date",
                                         value=datetime.now().date())
            start_time = st.time_input("Start Time",
                                       value=datetime.now().time())
            duration_minutes = st.number_input("Duration (minutes)",
                                               min_value=1, value=30)

            # Calculate end time based on duration
            start_datetime = datetime.combine(workout_date, start_time)
            end_datetime = start_datetime + timedelta(minutes=duration_minutes)

            # Workout details
            max_hr = st.number_input("Maximum Heart Rate", min_value=0,
                                     max_value=250, value=150)

            # Run intervals
            st.write("Running Intervals")
            num_intervals = st.number_input("Number of Intervals", min_value=1,
                                            max_value=10, value=1)

            intervals = []
            for i in range(num_intervals):
                st.write(f"Interval {i + 1}")
                col1, col2, col3 = st.columns(3)

                with col1:
                    distance = st.number_input(f"Distance (km)",
                                               min_value=0.0,
                                               max_value=100.0,
                                               value=1.0,
                                               step=0.1,
                                               key=f"dist_{i}")

                with col2:
                    minutes = st.number_input(f"Pace (minutes)",
                                              min_value=0,
                                              max_value=30,
                                              value=5,
                                              key=f"min_{i}")
                    seconds = st.number_input(f"Pace (seconds)",
                                              min_value=0,
                                              max_value=59,
                                              value=0,
                                              key=f"sec_{i}")
                    pace = f"{minutes:02d}:{seconds:02d}"

                with col3:
                    incline = st.number_input(f"Incline (%)",
                                              min_value=0.0,
                                              max_value=30.0,
                                              value=0.0,
                                              step=0.1,
                                              key=f"inc_{i}")

                intervals.append({
                    "interval_nr": i + 1,
                    "distance": distance,
                    "pace": pace,
                    "incline": incline
                })

            submit_button = st.form_submit_button("Add Running Workout")

            if submit_button:
                result = add_workout(
                    user_id,
                    start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    max_hr,
                    "Run"
                )

                if result["success"]:
                    workout_id = result["workout_id"]

                    # Then add all intervals
                    all_intervals_success = True
                    for interval in intervals:
                        interval_result = add_run_interval(
                            workout_id,
                            interval["interval_nr"],
                            interval["distance"],
                            interval["pace"],
                            interval["incline"]
                        )
                        if not interval_result["success"]:
                            st.error(
                                f"Error adding interval {interval['interval_nr']}: {interval_result['error']}")
                            all_intervals_success = False

                    if all_intervals_success:
                        st.success("Running workout added successfully!")
                        st.rerun()
                else:
                    st.error(f"Error adding workout: {result['error']}")

    # Tab 2: Weightlifting Workout
    with tab2:
        with st.form("add_weightlift_workout_form"):
            st.write("Create a new weightlifting workout")
            user_id = st.selectbox("User", user_ids, key="weightlift_user")

            # Date and time selection
            workout_date = st.date_input("Workout Date",
                                         value=datetime.now().date(),
                                         key="wl_date")
            start_time = st.time_input("Start Time",
                                       value=datetime.now().time(),
                                       key="wl_start")
            duration_minutes = st.number_input("Duration (minutes)",
                                               min_value=1, value=60,
                                               key="wl_duration")

            # Calculate end time
            start_datetime = datetime.combine(workout_date, start_time)
            end_datetime = start_datetime + timedelta(minutes=duration_minutes)

            # Workout details
            max_hr = st.number_input("Maximum Heart Rate", min_value=0,
                                     max_value=250, value=130, key="wl_hr")

            # Get exercises
            exercises_result = get_exercises()

            if not exercises_result["success"]:
                st.error(
                    f"Error loading exercises: {exercises_result['error']}")
                exercises = []
            else:
                exercises = exercises_result["exercises"]

            if not exercises:
                st.warning(
                    "No exercises found in the database. ")
            else:
                # Exercise selection
                st.write("Exercises")
                num_exercises = st.number_input("Number of Exercises",
                                                min_value=1, max_value=10,
                                                value=3)

                exercise_sets = []
                for i in range(num_exercises):
                    st.write(f"Exercise {i + 1}")

                    exercise_id = st.selectbox(
                        f"Exercise",
                        options=[ex["id"] for ex in exercises],
                        format_func=lambda x: next(
                            (ex["name"] + " (" + ex["muscleGroup"] + ")" for ex
                             in exercises if ex["id"] == x), ""),
                        key=f"ex_{i}"
                    )

                    num_sets = st.number_input(f"Number of Sets", min_value=1,
                                               max_value=10, value=3,
                                               key=f"sets_{i}")

                    for j in range(num_sets):
                        col1, col2 = st.columns(2)

                        with col1:
                            reps = st.number_input(f"Set {j + 1} Reps",
                                                   min_value=1,
                                                   max_value=100,
                                                   value=10,
                                                   key=f"reps_{i}_{j}")

                        with col2:
                            weight = st.number_input(f"Set {j + 1} Weight (kg)",
                                                     min_value=0.0,
                                                     max_value=500.0,
                                                     value=20.0,
                                                     step=2.5,
                                                     key=f"weight_{i}_{j}")

                        exercise_sets.append({
                            "exercise_id": exercise_id,
                            "set_nr": j + 1,
                            "reps": reps,
                            "weight": weight
                        })

            submit_button = st.form_submit_button(
                "Add Weightlifting Workout")

            if submit_button:
                # First add the workout
                result = add_workout(
                    user_id,
                    start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    max_hr,
                    "Weightlift"
                )

                if result["success"]:
                    workout_id = result["workout_id"]

                    # Then add all sets
                    all_sets_success = True
                    for ex_set in exercise_sets:
                        set_result = add_weightlift_set(
                            workout_id,
                            ex_set["exercise_id"],
                            ex_set["set_nr"],
                            ex_set["reps"],
                            ex_set["weight"]
                        )
                        if not set_result["success"]:
                            st.error(
                                f"Error adding set: {set_result['error']}")
                            all_sets_success = False

                    if all_sets_success:
                        st.success(
                            "Weightlifting workout added successfully!")
                        st.rerun()
                else:
                    st.error(f"Error adding workout: {result['error']}")

    # Delete operation
    st.subheader("Delete Workout")
    if not workouts_df.empty:
        with st.form("delete_workout_form"):
            workout_id = st.selectbox(
                "Select Workout to Delete",
                options=workouts_df['workoutID'].tolist(),
                format_func=lambda
                    x: f"Workout {x} - {workouts_df[workouts_df['workoutID'] == x]['workoutType'].iloc[0]} - {workouts_df[workouts_df['workoutID'] == x]['startTime'].iloc[0]}"
            )

            submit_button = st.form_submit_button("Delete Workout")

            if submit_button:
                result = delete_workout(workout_id)
                if result["success"]:
                    st.success("Workout deleted successfully!")
                    st.rerun()
                else:
                    st.error(f"Error deleting workout: {result['error']}")
    else:
        st.info("No workouts available to delete.")
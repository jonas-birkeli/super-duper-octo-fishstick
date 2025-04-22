import streamlit as st
import pandas as pd
from models.exercise import (
    get_all_exercises,
    add_exercise,
    update_exercise,
    delete_exercise,
    get_exercise_by_id
)


def exercises_page():
    """Exercise management page - CRUD operations for exercises"""
    st.header("Exercise Management")

    # Read operation - display all exercises
    exercises_df = get_all_exercises()
    st.write("Current Exercises:")
    st.dataframe(exercises_df)

    # Create operation - add new exercise
    st.subheader("Add New Exercise")
    with st.form("add_exercise_form"):
        name = st.text_input("Exercise Name")
        muscle_groups = [
            "Chest", "Back", "Legs", "Shoulders", "Arms",
            "Core", "Full Body", "Cardio", "Other"
        ]
        muscle_group = st.selectbox("Muscle Group", muscle_groups)

        submit_button = st.form_submit_button("Add Exercise")
        if submit_button:
            if not name:
                st.error("Exercise name is required")
            else:
                result = add_exercise(name, muscle_group)
                if result["success"]:
                    st.success(f"Exercise '{name}' added successfully!")
                    st.rerun()
                else:
                    st.error(f"Error adding exercise: {result['error']}")

    # Update operation
    if not exercises_df.empty:
        st.subheader("Update Exercise")
        with st.form("update_exercise_form"):
            exercise_id = st.selectbox(
                "Select Exercise",
                options=exercises_df['exerciseID'].tolist(),
                format_func=lambda
                    x: f"{exercises_df[exercises_df['exerciseID'] == x]['name'].iloc[0]} ({exercises_df[exercises_df['exerciseID'] == x]['muscleGroup'].iloc[0]})",
                key="update_exercise"
            )

            exercise_data = get_exercise_by_id(exercise_id)

            # Only proceed if we got data back
            if not exercise_data.empty:
                exercise_row = exercise_data.iloc[0]

                update_name = st.text_input("Exercise Name",
                                            value=exercise_row['name'])
                muscle_groups = [
                    "Chest", "Back", "Legs", "Shoulders", "Arms",
                    "Core", "Full Body", "Cardio", "Other"
                ]
                # Find index of current muscle group or default to 0
                current_muscle_index = next(
                    (i for i, mg in enumerate(muscle_groups) if
                     mg == exercise_row['muscleGroup']), 0)
                update_muscle_group = st.selectbox(
                    "Muscle Group",
                    muscle_groups,
                    index=current_muscle_index
                )

                submit_button = st.form_submit_button("Update Exercise")
                if submit_button:
                    if not update_name:
                        st.error("Exercise name is required")
                    else:
                        result = update_exercise(exercise_id, update_name,
                                                 update_muscle_group)
                        if result["success"]:
                            st.success("Exercise updated successfully!")
                            st.rerun()
                        else:
                            st.error(
                                f"Error updating exercise: {result['error']}")

    # Delete
    if not exercises_df.empty:
        st.subheader("Delete Exercise")
        with st.form("delete_exercise_form"):
            exercise_id = st.selectbox(
                "Select Exercise to Delete",
                options=exercises_df['exerciseID'].tolist(),
                format_func=lambda
                    x: f"{exercises_df[exercises_df['exerciseID'] == x]['name'].iloc[0]} ({exercises_df[exercises_df['exerciseID'] == x]['muscleGroup'].iloc[0]})",
                key="delete_exercise"
            )
            st.warning(
                "Note: You cannot delete exercises that are used in existing workouts.")
            submit_button = st.form_submit_button("Delete Exercise")

            if submit_button:
                result = delete_exercise(exercise_id)
                if result["success"]:
                    st.success("Exercise deleted successfully!")
                    st.rerun()
                else:
                    st.error(f"Error deleting exercise: {result['error']}")
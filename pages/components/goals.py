import streamlit as st
import pandas as pd
from datetime import datetime
from models.user import get_user_ids
from models.goals import (
    get_all_goals,
    get_goals_by_user,
    add_goal,
    update_goal,
    delete_goal,
    get_common_goal_names,
    get_common_metrics
)


def goals_page():
    """Goals management page - CRUD operations for fitness goals"""
    st.header("Goal Tracking")

    # Read operation - display all goals
    goals_df = get_all_goals()

    if not goals_df.empty:
        # Format the completed column for better display
        goals_df['Status'] = goals_df['completed'].apply(
            lambda x: '✅ Completed' if x == 1 else '⏳ In Progress')
        display_df = goals_df[
            ['userID', 'userName', 'goalName', 'amount', 'metric', 'Status']]
        display_df.columns = ['User ID', 'User Name', 'Goal', 'Amount',
                              'Metric', 'Status']

        st.write("Current Goals:")
        st.dataframe(display_df)
    else:
        st.info("No goals found. Add your first fitness goal below!")

    # Create operation - add new goal
    st.subheader("Add New Goal")

    # Get users for dropdown
    user_ids = get_user_ids()

    if not user_ids:
        st.warning("No users found. Please add a user first.")
        return

    with st.form("add_goal_form"):
        col1, col2 = st.columns(2)

        with col1:
            # Get user selection
            user_id = st.selectbox("User", user_ids, key="goal_user_add")

            # Common goal names for easier selection
            goal_options = get_common_goal_names()
            goal_name = st.selectbox("Goal Type", options=goal_options)

            # Option to enter custom goal name
            custom_goal = st.checkbox("Custom Goal Name")
            if custom_goal:
                goal_name = st.text_input("Enter Custom Goal Name")

        with col2:
            # Goal details
            amount = st.number_input("Target Amount", min_value=0.1, value=10.0,
                                     step=0.1)

            # Common metrics for easier selection
            metric_options = get_common_metrics()
            metric = st.selectbox("Metric", options=metric_options)

            # Default to not completed
            completed = st.checkbox("Mark as Completed")

        submit_button = st.form_submit_button("Add Goal")
        if submit_button:
            if not goal_name:
                st.error("Goal name is required")
            else:
                result = add_goal(user_id, goal_name, amount, metric,
                                  1 if completed else 0)
                if result["success"]:
                    st.success(f"Goal added successfully!")
                    st.rerun()
                else:
                    st.error(f"Error adding goal: {result['error']}")

    # Update operation - update goal status
    if not goals_df.empty:
        st.subheader("Update Goal")

        with st.form("update_goal_form"):
            # First select the user
            user_id = st.selectbox("Select User", user_ids,
                                   key="goal_user_update")

            # Get goals for selected user
            user_goals_df = get_goals_by_user(user_id)

            if user_goals_df.empty:
                st.info("This user has no goals yet.")
                submit_button = st.form_submit_button("Update Goal",
                                                      disabled=True)
            else:
                # Then select the goal
                goal_options = user_goals_df['goalName'].tolist()
                goal_name = st.selectbox("Select Goal", goal_options)

                # Get current goal data
                goal_row = \
                user_goals_df[user_goals_df['goalName'] == goal_name].iloc[0]

                col1, col2 = st.columns(2)

                with col1:
                    update_amount = st.number_input("Target Amount",
                                                    min_value=0.1,
                                                    value=float(
                                                        goal_row['amount']),
                                                    step=0.1)

                    metric_options = get_common_metrics()
                    current_metric_index = metric_options.index(
                        goal_row['metric']) if goal_row[
                                                   'metric'] in metric_options else 0
                    update_metric = st.selectbox("Metric",
                                                 options=metric_options,
                                                 index=current_metric_index)

                with col2:
                    update_completed = st.checkbox("Mark as Completed",
                                                   value=True if goal_row[
                                                                     'completed'] == 1 else False)

                    # Progress visualization if not completed
                    if not update_completed:
                        progress_percent = st.slider("Progress (%)", 0, 100, 50)
                        st.progress(progress_percent / 100)

                submit_button = st.form_submit_button("Update Goal")
                if submit_button:
                    result = update_goal(user_id, goal_name, update_amount,
                                         update_metric,
                                         1 if update_completed else 0)
                    if result["success"]:
                        st.success(f"Goal updated successfully!")
                        st.rerun()
                    else:
                        st.error(f"Error updating goal: {result['error']}")

    # Delete operation - remove goal
    if not goals_df.empty:
        st.subheader("Delete Goal")

        with st.form("delete_goal_form"):
            # First select the user
            user_id = st.selectbox("Select User", user_ids,
                                   key="goal_user_delete")

            # Get goals for selected user
            user_goals_df = get_goals_by_user(user_id)

            if user_goals_df.empty:
                st.info("This user has no goals to delete.")
                submit_button = st.form_submit_button("Delete Goal",
                                                      disabled=True)
            else:
                # Then select the goal to delete
                goal_options = user_goals_df['goalName'].tolist()
                goal_name = st.selectbox("Select Goal to Delete", goal_options)

                submit_button = st.form_submit_button("Delete Goal")
                if submit_button:
                    result = delete_goal(user_id, goal_name)
                    if result["success"]:
                        st.success("Goal deleted successfully!")
                        st.rerun()
                    else:
                        st.error(f"Error deleting goal: {result['error']}")
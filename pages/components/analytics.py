import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from models.analysis import get_user_progress_overview, \
    get_exercise_effectiveness_analysis


def analytics_page():
    """Analytics page with data visualizations from database views"""
    st.header("Advanced Analytics")

    tab1, tab2 = st.tabs(
        ["User Progress Overview", "Exercise Effectiveness Analysis"])

    # Tab 1: User Progress Overview
    with tab1:
        st.subheader("User Progress Overview")
        progress_result = get_user_progress_overview()

        if progress_result["success"] and not progress_result["data"].empty:

            st.write("User Progress Data:")
        else:
            if not progress_result["success"]:
                st.error(
                    f"Error retrieving user progress data: {progress_result.get('error', 'Unknown error')}")
            else:
                st.info(
                    "No user progress data available. Please add users, workouts, and health records first.")

    # Tab 2: Exercise effectiveness
    with tab2:
        st.subheader("Exercise Effectiveness Analysis")
        effectiveness_result = get_exercise_effectiveness_analysis()

        if effectiveness_result["success"] and not effectiveness_result["data"].empty:

            st.write("Exercise Effectiveness Data:")
        else:
            if not effectiveness_result["success"]:
                st.error(
                    f"Error retrieving exercise effectiveness data: {effectiveness_result.get('error', 'Unknown error')}")
            else:
                st.info(
                    "No exercise effectiveness data available. Please add exercises and weightlifting workouts first.")
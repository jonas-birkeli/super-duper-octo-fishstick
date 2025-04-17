import streamlit as st
import plotly.express as px
from models.workout import get_workout_statistics


def dashboard_page():
    """Dashboard page with data visualization"""
    st.header("Data Visualization")

    stats_result = get_workout_statistics()

    if stats_result["success"] and not stats_result["data"].empty:
        df = stats_result["data"]

        st.subheader("Average Workout Duration by User and Type")

        # Very simple plotly over workouts
        fig = px.bar(
            df,
            x='userName',
            y='avgDurationMinutes',
            color='workoutType',
            labels={
                'userName': 'User Name',
                'avgDurationMinutes': 'Average Duration (minutes)',
                'workoutType': 'Workout Type'
            },
            title='Average Workout Duration per User by Workout Type'
        )

        st.plotly_chart(fig)

        # Raw data
        st.subheader("Raw Data")
        st.dataframe(df)
    else:
        if not stats_result["success"]:
            st.error(
                f"Error retrieving statistics: {stats_result.get('error', 'Unknown error')}")
        else:
            st.info(
                "No workout data available for visualization. Please add some workouts first.")
import streamlit as st
from models.health import get_all_health_records, add_health_record, delete_health_record
from models.user import get_user_ids

def health_page():
    """Health records management page - CRUD operations for health records"""
    st.header("Health Records")

    health_df = get_all_health_records()
    st.write("Current Health Records:")
    st.dataframe(health_df)

    st.subheader("Add New Health Record")
    user_ids = get_user_ids()

    # Add
    if user_ids:
        with st.form("add_health_form"):
            user_id = st.selectbox("User ID", user_ids, key="add_health_user")
            date = st.date_input("Date")
            heartrate = st.number_input("Heart Rate", value=70, min_value=0)
            vo2max = st.number_input("VO2 Max", value=40.0, min_value=0.0)
            hrvariation = st.number_input("HR Variation", value=10, min_value=0)
            sleeptime = st.number_input("Sleep Time (hours)", value=8.0, min_value=0.0, max_value=24.0)

            submit_button = st.form_submit_button("Add Health Record")
            if submit_button:
                result = add_health_record(
                    user_id, date.strftime("%Y-%m-%d"), heartrate, vo2max, hrvariation, sleeptime
                )
                if result["success"]:
                    st.success("Health record added successfully!")
                    st.experimental_rerun()
                else:
                    st.error(f"Error adding health record: {result['error']}")
    else:
        st.info("No users available. Please add a user first.")

    # Orker ikke update fordi vi bruker foreign keys

    # Delete
    st.subheader("Delete Health Record")
    if not health_df.empty:
        with st.form("delete_health_form"):
            # Create a list of user_id + date options for selection
            health_options = [f"{row['userID']}: {row['date']}" for _, row in health_df.iterrows()]
            selected_option = st.selectbox("Select Record to Delete", health_options)

            submit_button = st.form_submit_button("Delete Record")

            if submit_button:
                # Parsing
                user_id, date = selected_option.split(": ")
                result = delete_health_record(int(user_id), date)
                if result["success"]:
                    st.success("Deleted health record successfully!")
                    st.experimental_rerun()
                else:
                    st.error(f"Error deleting health record: {result['error']}")
    else:
        st.info("No health records available to delete.")
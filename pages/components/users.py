import streamlit as st
from datetime import datetime
from models.user import get_all_users, add_user, update_user, delete_user, \
    get_user_by_id, get_user_ids


def users_page():
    """User management page - CRUD operations for users"""
    st.header("Users")

    users_df = get_all_users()
    st.write("Current Users:")
    st.dataframe(users_df)

    # Add
    st.subheader("Add New User")
    with st.form("add_user_form"):
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        weight = st.number_input("Weight", min_value=0.1, value=70.0, step=0.1)
        dob = st.date_input("Date of Birth", min_value=datetime(1900, 1, 1), max_value=datetime.now())
        sex = st.selectbox("Sex", ["M", "F"])

        submit_button = st.form_submit_button("Add User")
        if submit_button:
            result = add_user(
                fname, lname, weight, dob.strftime("%Y-%m-%d"), sex
            )
            if result["success"]:
                st.success("User added successfully!")
                st.experimental_rerun()
            else:
                st.error(f"Error adding user: {result['error']}")

    # Update
    st.subheader("Update User")
    user_ids = get_user_ids()

    if user_ids:
        with st.form("update_user_form"):
            user_id = st.selectbox("Select User ID", user_ids,
                                   key="update_user")

            # Get current user data
            user_data = get_user_by_id(user_id)

            # Only continue if we got data back
            if not user_data.empty:
                user_row = user_data.iloc[0]

                update_fname = st.text_input("First Name",
                                             value=user_row['fName'])
                update_lname = st.text_input("Last Name",
                                             value=user_row['lName'])
                update_weight = st.number_input("Weight", min_value=0.1,
                                                value=float(user_row['weight']),
                                                step=0.1)

                # Handle date format
                try:
                    current_dob = datetime.strptime(user_row['DOB'],
                                                    "%Y-%m-%d").date() if \
                    user_row['DOB'] else datetime.now().date()
                except:
                    current_dob = datetime.now().date()

                update_dob = st.date_input("Date of Birth", value=current_dob)
                update_sex = st.selectbox("Sex", ["M", "F"],
                                          index=0 if user_row[
                                                         'sex'] == 'M' else 1)

                submit_button = st.form_submit_button("Update User")
                if submit_button:
                    result = update_user(
                        user_id, update_fname, update_lname, update_weight,
                        update_dob.strftime("%Y-%m-%d"), update_sex
                    )
                    if result["success"]:
                        st.success("User updated successfully!")
                        st.experimental_rerun()
                    else:
                        st.error(f"Error updating user: {result['error']}")

    # Delete
    st.subheader("Delete User")
    user_ids = get_user_ids()

    if user_ids:
        with st.form("delete_user_form"):
            user_id = st.selectbox("Select User ID to Delete", user_ids,
                                   key="delete_user")
            st.warning(
                "Warning: Deleting a user will also delete all associated records (health, workouts, goals).")
            submit_button = st.form_submit_button("Delete User")

            if submit_button:
                result = delete_user(user_id)
                if result["success"]:
                    st.success("User deleted successfully!")
                    st.experimental_rerun()
                else:
                    st.error(f"Error deleting user: {result['error']}")
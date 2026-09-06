import streamlit as st

import auth
import database

st.set_page_config(
    page_title="Meditrak | My Account",
    page_icon="👤",
    layout="wide"
)

auth.require_login()
auth.logout_button()

st.title("My Account")

username = st.session_state.username
user = database.get_user(username)

st.subheader("Profile")

col1, col2 = st.columns(2)
col1.metric("Username", username)

if user:
    joined = user["created_at"].split("T")[0]
    col2.metric("Member Since", joined)

st.divider()

st.subheader("Your Activity")

history_df = database.get_predictions(username=username)

st.metric("Total Predictions Made", len(history_df))

if not history_df.empty:
    st.write("Demand levels you've predicted most often:")
    st.bar_chart(history_df["demand_level"].value_counts())

st.divider()

st.subheader("Log Out")
st.write("Use the button in the sidebar to log out of your account.")

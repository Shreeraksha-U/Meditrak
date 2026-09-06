import streamlit as st

import auth
import database

st.set_page_config(
    page_title="Meditrak | Prediction History",
    page_icon="📜",
    layout="wide"
)

auth.require_login()
auth.logout_button()

st.title("Prediction History")
st.write("Every demand forecast you've generated, saved for future reference.")

username = st.session_state.username

history_df = database.get_predictions(username=username)

if history_df.empty:
    st.info("You haven't made any predictions yet. Head to the main page to get started.")
else:

    # FILTERS

    left, right = st.columns(2)

    with left:
        store_filter = st.multiselect(
            "Filter by Store",
            sorted(history_df["store"].unique())
        )

    with right:
        demand_filter = st.multiselect(
            "Filter by Demand Level",
            sorted(history_df["demand_level"].unique())
        )

    filtered_df = history_df.copy()

    if store_filter:
        filtered_df = filtered_df[filtered_df["store"].isin(store_filter)]

    if demand_filter:
        filtered_df = filtered_df[filtered_df["demand_level"].isin(demand_filter)]

    st.metric("Predictions Shown", len(filtered_df))

    st.dataframe(
        filtered_df[
            [
                "id", "store", "medicine", "category", "price",
                "forecast_date", "promotion", "holiday",
                "predicted_units", "demand_level", "created_at"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Remove a Prediction")

    delete_id = st.number_input(
        "Prediction ID to delete",
        min_value=0,
        step=1
    )

    if st.button("Delete"):
        if delete_id in filtered_df["id"].values:
            database.delete_prediction(int(delete_id), username)
            st.success(f"Prediction #{delete_id} deleted.")
            st.rerun()
        else:
            st.error("That prediction ID doesn't belong to you or doesn't exist.")

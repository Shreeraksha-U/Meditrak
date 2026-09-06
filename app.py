import streamlit as st
import pandas as pd

from predict import predict_demand
from datetime import date

import auth
import database
import utils

# INIT DATABASE

database.init_db()

st.set_page_config(
    page_title="Meditrak Demand Forecasting",
    page_icon="M",
    layout="wide"
)

# AUTH GATE
# Shows Login / Sign Up tabs until the user is authenticated.

if not auth.auth_gate():
    st.stop()

auth.logout_button()

st.title("Meditrak Demand Forecasting")

st.write(
    "Predict future medicine demand using Machine Learning."
)

# LOAD DATASET

df = pd.read_csv(
    "dataset/medicine_sales_processed.csv"
)

# CREATE TWO COLUMNS

left, right = st.columns(2)


# LEFT COLUMN

with left:

    # Directly use the store names from your dataset
    store = st.selectbox(
        "Store",
        sorted(df["Store_ID"].unique())
    )

    medicine = st.selectbox(
        "Medicine",
        sorted(df["Medicine_Name"].unique())
    )

    date = st.date_input(
        "Select Forecast Date",
        min_value=date.today()
    )

# GET MEDICINE DETAILS

row = df[
    df["Medicine_Name"] == medicine
].iloc[0]

item_id = row["Item_ID"]

category = row["Category"]

price = row["Base_Price"]

# RIGHT COLUMN

with right:

    promotion = st.checkbox(
        "Promotion"
    )

    holiday = st.checkbox(
        "Holiday"
    )

# CREATE DATE FEATURES

day = date.strftime("%A")

month = date.strftime("%B")

weekend = 1 if date.weekday() >= 5 else 0

# PREDICT BUTTON

if st.button("Predict Demand"):

    prediction = predict_demand(
        store,
        item_id,
        medicine,
        category,
        price,
        int(promotion),
        int(holiday),
        day,
        month,
        weekend
    )

# Show prediction
    st.success(
        f"Predicted Demand: {prediction:.0f} Units"
    )

# DEMAND RECOMMENDATION

    level, recommendation, alert_type = utils.categorize_demand(prediction)

    getattr(st, alert_type)(
        f"{level} Demand\n\n{recommendation}"
    )

# SAVE TO PREDICTION HISTORY

    database.save_prediction(
        username=st.session_state.username,
        store=store,
        medicine=medicine,
        item_id=item_id,
        category=category,
        price=float(price),
        promotion=promotion,
        holiday=holiday,
        forecast_date=date.strftime("%Y-%m-%d"),
        day_of_week=day,
        month=month,
        is_weekend=weekend,
        predicted_units=float(prediction),
        demand_level=level
    )

    st.caption("Saved to your Prediction History (see sidebar pages).")

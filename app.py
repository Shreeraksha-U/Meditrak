import streamlit as st
import pandas as pd

from predict import predict_demand
from datetime import date

st.set_page_config(
    page_title="Meditrak Demand Forecasting",
    page_icon="M",
    layout="wide"
)

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
    if prediction < 40:

        st.warning(
            "Low Demand\n\n"
            "Maintain minimum inventory."
        )

    elif prediction < 90:

        st.info(
            "Moderate Demand\n\n"
            "Maintain regular stock."
        )

    elif prediction < 140:

        st.success(
            "High Demand\n\n"
            "Increase inventory."
        )

    else:

        st.error(
            "Very High Demand\n\n"
            "Place replenishment order immediately."
        )
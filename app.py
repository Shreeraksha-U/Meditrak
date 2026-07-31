import streamlit as st
import pandas as pd

from predict import predict_demand

st.set_page_config(
    page_title="Meditrak Demand Forecasting",
    page_icon="🏥",
    layout="wide"
)

st.title("Meditrak Demand Forecasting")
st.write(
    "Predict future medicine demand using Machine Learning."
)

df = pd.read_csv("dataset/medicine_sales_processed.csv")

left, right = st.columns(2)

with left:

    store = st.selectbox(
        "Store",
        sorted(df["Store_ID"].unique())
    )

    medicine = st.selectbox(
        "Medicine",
        sorted(df["Medicine_Name"].unique())
    )

    date = st.date_input("Select Date")

    row = df[df["Medicine_Name"] == medicine].iloc[0]

    item_id = row["Item_ID"]

    category = row["Category"]

    price = row["Base_Price"]

with right:

    promotion = st.checkbox("Promotion")

    holiday = st.checkbox("Holiday")

day = date.strftime("%A")

month = date.strftime("%B")

weekend = 1 if date.weekday() >= 5 else 0

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

    st.success(
        f"Predicted Demand : {prediction:.0f} Units"
    )
    if prediction < 40:

        st.warning(
            "Low Demand\n\nMaintain minimum inventory."
        )

    elif prediction < 90:

        st.info(
            "Moderate Demand\n\nMaintain regular stock."
        )

    elif prediction < 140:

        st.success(
            "High Demand\n\nIncrease inventory."
        )

    else:

        st.error(
            "Very High Demand\n\nPlace replenishment order immediately."
        )

st.subheader("Model Performance")

with open("models/model_metrics.txt") as f:

    st.code(f.read())

st.subheader("Actual vs Predicted")

st.image(
    "images/actual_vs_predicted.png",
    use_container_width=True
)
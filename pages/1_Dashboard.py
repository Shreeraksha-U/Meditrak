import streamlit as st
import pandas as pd

import auth
import database

st.set_page_config(
    page_title="Meditrak | Dashboard",
    page_icon="📊",
    layout="wide"
)

auth.require_login()
auth.logout_button()

st.title("Dashboard")
st.write("Sales analytics and a summary of demand predictions made so far.")

# LOAD SALES DATASET

sales_df = pd.read_csv("dataset/medicine_sales_processed.csv")

# LOAD PREDICTION HISTORY (ALL USERS)

predictions_df = database.get_predictions()

# -------------------------------
# TOP LEVEL METRICS
# -------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales Records", f"{len(sales_df):,}")
col2.metric("Stores Tracked", sales_df["Store_ID"].nunique())
col3.metric("Medicines Tracked", sales_df["Medicine_Name"].nunique())
col4.metric("Predictions Made", f"{len(predictions_df):,}")

st.divider()

# -------------------------------
# SALES ANALYTICS
# -------------------------------

left, right = st.columns(2)

with left:
    st.subheader("Average Units Sold by Category")

    category_avg = (
        sales_df.groupby("Category")["Units_Sold"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_avg)

with right:
    st.subheader("Average Units Sold by Store")

    store_avg = (
        sales_df.groupby("Store_ID")["Units_Sold"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(store_avg)

st.subheader("Average Units Sold by Day of Week")

day_order = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]

day_avg = (
    sales_df.groupby("Day_of_Week")["Units_Sold"]
    .mean()
    .reindex(day_order)
)

st.bar_chart(day_avg)

st.subheader("Top 10 Best Selling Medicines")

top_medicines = (
    sales_df.groupby("Medicine_Name")["Units_Sold"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_medicines)

st.divider()

# -------------------------------
# PREDICTION ANALYTICS
# -------------------------------

st.subheader("Predicted Demand Levels (All Users)")

if predictions_df.empty:
    st.info("No predictions have been made yet. Head to the main page to generate one.")
else:
    demand_counts = predictions_df["demand_level"].value_counts()
    st.bar_chart(demand_counts)

    st.subheader("Recent Predictions")
    st.dataframe(
        predictions_df[
            [
                "username", "store", "medicine", "forecast_date",
                "predicted_units", "demand_level", "created_at"
            ]
        ].head(20),
        use_container_width=True
    )

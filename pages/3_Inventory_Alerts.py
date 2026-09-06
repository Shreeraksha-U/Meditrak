import streamlit as st
import pandas as pd

import auth

st.set_page_config(
    page_title="Meditrak | Inventory Alerts",
    page_icon="📦",
    layout="wide"
)

auth.require_login()
auth.logout_button()

st.title("Inventory Alerts")
st.write(
    "Enter your current stock for a store's medicines and Meditrak will flag "
    "items likely to run out soon, based on historical average daily demand."
)

sales_df = pd.read_csv("dataset/medicine_sales_processed.csv")

# STORE SELECTION

store = st.selectbox(
    "Store",
    sorted(sales_df["Store_ID"].unique())
)

reorder_days = st.slider(
    "Alert if stock will run out within this many days",
    min_value=1,
    max_value=30,
    value=7
)

# AVERAGE DAILY DEMAND PER MEDICINE FOR THE SELECTED STORE

store_df = sales_df[sales_df["Store_ID"] == store]

avg_demand = (
    store_df.groupby("Medicine_Name")["Units_Sold"]
    .mean()
    .round(1)
    .reset_index()
    .rename(columns={"Units_Sold": "Avg_Daily_Demand"})
)

avg_demand["Current_Stock"] = 0

st.subheader(f"Enter Current Stock for {store}")

edited = st.data_editor(
    avg_demand,
    column_config={
        "Medicine_Name": st.column_config.TextColumn("Medicine", disabled=True),
        "Avg_Daily_Demand": st.column_config.NumberColumn("Avg Daily Demand", disabled=True),
        "Current_Stock": st.column_config.NumberColumn("Current Stock (units)", min_value=0, step=1),
    },
    hide_index=True,
    use_container_width=True
)

# CALCULATE DAYS OF STOCK REMAINING

edited["Days_Remaining"] = edited.apply(
    lambda r: round(r["Current_Stock"] / r["Avg_Daily_Demand"], 1)
    if r["Avg_Daily_Demand"] > 0 else float("inf"),
    axis=1
)

low_stock = edited[edited["Days_Remaining"] <= reorder_days]

st.divider()

if low_stock.empty:
    st.success("No medicines are currently at risk of stocking out.")
else:
    st.error(f"{len(low_stock)} medicine(s) need restocking soon:")

    st.dataframe(
        low_stock[["Medicine_Name", "Current_Stock", "Avg_Daily_Demand", "Days_Remaining"]]
        .sort_values("Days_Remaining"),
        use_container_width=True,
        hide_index=True
    )

    for _, r in low_stock.sort_values("Days_Remaining").iterrows():
        st.warning(
            f"**{r['Medicine_Name']}** — approximately "
            f"{r['Days_Remaining']} day(s) of stock left at current demand. "
            "Place a replenishment order."
        )

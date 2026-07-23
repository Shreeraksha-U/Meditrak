import pandas as pd
df = pd.read_csv("dataset/medicine_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Day_of_Week"] = df["Date"].dt.day_name()
df["Month"] = df["Date"].dt.month_name()
df["Is_Weekend"] = df["Date"].dt.weekday >= 5
df["Is_Weekend"] = df["Is_Weekend"].astype(int)
print(df.head())
df.to_csv("dataset/medicine_sales_processed.csv", index=False)
import pandas as pd
from predict import predict_demand

df = pd.read_csv("dataset/medicine_sales_processed.csv")

medicines = df["Medicine_Name"].unique()
stores = df["Store_ID"].unique()

print("Available medicines:")
for i, medicine in enumerate(medicines):
    print(i, medicine)

print("\nAvailable stores:")
for i, store in enumerate(stores):
    print(i, store)
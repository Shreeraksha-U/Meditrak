import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def main():
    # -------------------------------
    # Create folders if they don't exist
    # -------------------------------
    os.makedirs("models", exist_ok=True)
    os.makedirs("images", exist_ok=True)

    # -------------------------------
    # Load dataset
    # -------------------------------
    df = pd.read_csv("dataset/medicine_sales_processed.csv")

    print("Dataset Loaded Successfully!\n")
    print(df.head())

    # -------------------------------
    # Encode categorical columns
    # -------------------------------
    categorical_columns = [
        "Store_ID",
        "Item_ID",
        "Medicine_Name",
        "Category",
        "Day_of_Week",
        "Month"
    ]

    encoders = {}

    for column in categorical_columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        encoders[column] = le

    # -------------------------------
    # Split Features & Target
    # -------------------------------
    X = df.drop(columns=["Units_Sold", "Date"])
    y = df["Units_Sold"]

    # -------------------------------
    # Train-Test Split
    # -------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    # -------------------------------
    # Train Model
    # -------------------------------
    model = LinearRegression()

    model.fit(X_train, y_train)

    # -------------------------------
    # Predictions
    # -------------------------------
    y_pred = model.predict(X_test)

    # -------------------------------
    # Evaluation Metrics
    # -------------------------------
    mae = mean_absolute_error(y_test, y_pred)

    mse = mean_squared_error(y_test, y_pred)

    rmse = mse ** 0.5

    r2 = r2_score(y_test, y_pred)

    print("\n========== MODEL PERFORMANCE ==========")
    print(f"MAE      : {mae:.2f}")
    print(f"MSE      : {mse:.2f}")
    print(f"RMSE     : {rmse:.2f}")
    print(f"R² Score : {r2:.4f}")

    # -------------------------------
    # Save Model
    # -------------------------------
    joblib.dump(model, "models/linear_regression_model.pkl")
    joblib.dump(encoders, "models/label_encoders.pkl")

    print("\nModel saved successfully!")

    # -------------------------------
    # Save Metrics
    # -------------------------------
    with open("models/model_metrics.txt", "w") as f:
        f.write("Meditrak Demand Forecasting\n")
        f.write("===========================\n\n")
        f.write(f"MAE      : {mae:.2f}\n")
        f.write(f"MSE      : {mse:.2f}\n")
        f.write(f"RMSE     : {rmse:.2f}\n")
        f.write(f"R² Score : {r2:.4f}\n")

    print("Model metrics saved!")

    # -------------------------------
    # Actual vs Predicted Graph
    # -------------------------------
    plt.figure(figsize=(8, 6))

    plt.scatter(y_test, y_pred)

    plt.plot(
        [y_test.min(), y_test.max()],
        [y_test.min(), y_test.max()],
        "r--",
        linewidth=2
    )

    plt.xlabel("Actual Units Sold")
    plt.ylabel("Predicted Units Sold")
    plt.title("Actual vs Predicted Sales")

    plt.tight_layout()

    plt.savefig("images/actual_vs_predicted.png")

    plt.show()

    print("Graph saved in images/actual_vs_predicted.png")
    
if __name__ == "__main__":
    main()
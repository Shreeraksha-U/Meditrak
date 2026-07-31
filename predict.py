import joblib
import pandas as pd


# Load model and encoders only once
model = joblib.load("models/linear_regression_model.pkl")
encoders = joblib.load("models/label_encoders.pkl")


def predict_demand(
    store,
    item_id,
    medicine,
    category,
    price,
    promotion,
    holiday,
    day,
    month,
    weekend
):
    sample = {
        "Store_ID": store,
        "Item_ID": item_id,
        "Medicine_Name": medicine,
        "Category": category,
        "Base_Price": price,
        "Promotion": promotion,
        "Holiday": holiday,
        "Day_of_Week": day,
        "Month": month,
        "Is_Weekend": weekend
    }

    df = pd.DataFrame([sample])

    categorical_columns = [
        "Store_ID",
        "Item_ID",
        "Medicine_Name",
        "Category",
        "Day_of_Week",
        "Month"
    ]

    for column in categorical_columns:
        df[column] = encoders[column].transform(df[column])

    prediction = model.predict(df)

    return round(prediction[0], 2)
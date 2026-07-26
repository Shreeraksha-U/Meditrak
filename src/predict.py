import joblib
import pandas as pd

#Load the model and encoders
model = joblib.load("models/linear_regression_model.pkl")
encoders = joblib.load("models/label_encoders.pkl")

#Create sample input
sample = {
    "Store_ID": "S001",
    "Item_ID": "M101",
    "Medicine_Name": "Paracetamol",
    "Category": "Painkiller",
    "Base_Price": 25,
    "Promotion": 1,
    "Holiday": 0,
    "Day_of_Week": "Monday",
    "Month": "July",
    "Is_Weekend": 0
}

input_df = pd.DataFrame([sample]) #Convert to DataFrame

#Encode categorical columns
categorical_columns = [
    "Store_ID",
    "Item_ID",
    "Medicine_Name",
    "Category",
    "Day_of_Week",
    "Month"
]

for column in categorical_columns:
    input_df[column] = encoders[column].transform(input_df[column])

#predict
prediction = model.predict(input_df)

print(f"Predicted Units Sold: {prediction[0]:.2f}")
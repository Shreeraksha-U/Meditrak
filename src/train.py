import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
#Loading dataset
df = pd.read_csv("dataset/medicine_sales_processed.csv")
print(df.head())

#creating encoder since ML model can't understand text and only understands numbers
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

#Separate Inputs and Output, Our target is Units_Sold
X = df.drop(columns=["Units_Sold", "Date"])
y = df["Units_Sold"]

#Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
model = LinearRegression() #Create model
model.fit(X_train, y_train) #Train model
y_pred = model.predict(X_test) #Predict
#comparing Actual Sales vs Predicted Sales

#evaluating the regression model
mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

rmse = mse ** 0.5

r2 = r2_score(y_test, y_pred)

#Results
print("\nModel Performance")

print(f"MAE  : {mae:.2f}")

print(f"MSE  : {mse:.2f}")

print(f"RMSE : {rmse:.2f}")

print(f"R² Score : {r2:.4f}") #A higher R² (closer to 1) generally means the model explains more of the variation in the target.

joblib.dump(model, "models/linear_regression_model.pkl") #Save model
joblib.dump(encoders, "models/label_encoders.pkl")
print("\nModel saved successfully!")
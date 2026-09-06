# Meditrak – Medicine Demand Forecasting System

Meditrak is a machine learning-based medicine demand forecasting system designed to help pharmacies predict future medicine demand and support better inventory planning.

The application uses a **Linear Regression** model to predict the expected number of units sold based on factors such as the store, medicine, price, promotion status, holiday status, and calendar-related features. It now also includes user accounts, a sales/analytics dashboard, saved prediction history, and low-stock inventory alerts.

## Problem Statement

Pharmacies need to maintain an appropriate level of inventory to avoid:

* Overstocking of medicines
* Stock shortages
* Unnecessary inventory costs
* Poor demand planning

Meditrak addresses this problem by predicting the expected demand for medicines based on historical synthetic sales data and relevant business factors.

## Features

* User sign up and login, with per-user accounts
* Predict future medicine demand
* Select pharmacy/store and medicine
* Select a future forecast date
* Consider promotion and holiday conditions
* Automatically extract calendar features
* Categorize predicted demand as Low, Moderate, High, or Very High
* Provide inventory recommendations
* Every prediction is saved to that user's Prediction History
* Dashboard with sales analytics and predicted-demand insights across all users
* Inventory Alerts page that flags medicines likely to run out soon
* Account page summarizing each user's profile and activity
* Display model performance metrics
* Visualize actual vs predicted sales
* Display sales analytics

## Machine Learning Model

The project uses **Linear Regression**, as required for the Meditrak demand forecasting model.

### Target Variable

```text
Units_Sold
```

### Input Features

The model uses the following features:

* Store_ID
* Item_ID
* Medicine_Name
* Category
* Base_Price
* Promotion
* Holiday
* Day_of_Week
* Month
* Is_Weekend

The `Date` column is used during preprocessing to generate calendar-related features and is not directly used as an input to the Linear Regression model.

## Dataset

The dataset used in this project is **synthetically generated** for educational purposes.

It contains pharmacy sales records with the following columns:

| Column        | Description                   |
| ------------- | ----------------------------- |
| Date          | Date of the sales record      |
| Store_ID      | Pharmacy/store identifier     |
| Item_ID       | Medicine identifier           |
| Medicine_Name | Name of the medicine          |
| Category      | Medicine category             |
| Base_Price    | Base price of the medicine    |
| Promotion     | Whether a promotion is active |
| Holiday       | Whether the day is a holiday  |
| Units_Sold    | Number of units sold          |

Additional features created during preprocessing:

* Day_of_Week
* Month
* Is_Weekend

## Machine Learning Workflow

```text
Synthetic Dataset Generation
            ↓
Data Preprocessing
            ↓
Feature Engineering
            ↓
Categorical Data Encoding
            ↓
Train-Test Split
            ↓
Linear Regression Model Training
            ↓
Model Evaluation
            ↓
Save Model and Encoders
            ↓
Streamlit Web Application
            ↓
Future Demand Prediction
```

## Model Evaluation

The Linear Regression model is evaluated using:

* Mean Absolute Error (MAE)
* Mean Squared Error (MSE)
* Root Mean Squared Error (RMSE)
* R² Score

The model performance from the current training run is:

```text
MAE: 7.81
MSE: 81.55
RMSE: 9.03
R² Score: 0.6845
```

## Demand Categories

The predicted demand is categorized into four levels:

| Predicted Units | Demand Level | Inventory Recommendation    |
| --------------- | ------------ | ---------------------------- |
| Below 40        | Low          | Maintain minimum inventory  |
| 40–89           | Moderate     | Maintain regular stock      |
| 90–139          | High         | Increase inventory          |
| 140 and above   | Very High    | Place a replenishment order |

## User Accounts

Meditrak requires an account before making predictions.

* New users can sign up with a username and password from the Sign Up tab on the main page.
* Passwords are never stored in plain text — each one is hashed with a per-user random salt (PBKDF2-HMAC-SHA256) before being saved.
* Returning users log in from the Log In tab.
* A **Log Out** button is available in the sidebar on every page.
* Accounts and saved predictions are stored locally in a SQLite database (`meditrak.db`), which is created automatically the first time the app runs.

## Dashboard

The **Dashboard** page gives an at-a-glance view of the sales data and prediction activity:

* Total sales records, stores, and medicines tracked
* Average units sold by category, store, and day of the week
* Top 10 best-selling medicines
* Breakdown of predicted demand levels across all users
* A table of the most recent predictions made in the app

## Prediction History

Every prediction made from the main page is automatically saved against the logged-in user's account. The **Prediction History** page lets a user:

* View all of their past predictions
* Filter by store or demand level
* Delete a prediction they no longer need

## Inventory Alerts

The **Inventory Alerts** page helps translate demand data into a restocking decision:

* Pick a store and enter the current stock on hand for each medicine
* Meditrak compares that stock against the historical average daily demand for that store
* Any medicine projected to run out within a configurable number of days (default 7) is flagged, with an estimate of how many days of stock remain

## Application Interface

The Streamlit application allows the user to:

1. Sign up or log in.
2. Select a pharmacy/store.
3. Select a medicine.
4. Select a future forecast date.
5. Specify whether a promotion is active.
6. Specify whether the selected date is a holiday.
7. Generate a predicted demand value.
8. View the demand category.
9. Receive an inventory recommendation.
10. Review the prediction later from the Prediction History page.

The selected date is converted into:

* Day of the week
* Month
* Weekend status

These features are then passed to the trained Linear Regression model.

## Project Structure

```text
Meditrak/
│
├── app.py
├── auth.py
├── database.py
├── utils.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Prediction_History.py
│   ├── 3_Inventory_Alerts.py
│   └── 4_My_Account.py
│
├── dataset/
│   ├── medicine_sales.csv
│   └── medicine_sales_processed.csv
│
├── models/
│   ├── linear_regression_model.pkl
│   ├── label_encoders.pkl
│   └── model_metrics.txt
│
├── images/
│   └── actual_vs_predicted.png
│
├── notebooks/
│   └── eda.ipynb
│
├── generate_dataset.py
├── preprocess.py
├── train.py
├── predict.py
├── test_predictions.py
│
└── meditrak.db   (created automatically on first run)
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

### 2. Navigate to the project folder

```bash
cd Meditrak
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

No additional packages are required for authentication or storage — these use Python's built-in `sqlite3`, `hashlib`, and `secrets` modules.

## Running the Project

### Generate the synthetic dataset

```bash
python generate_dataset.py
```

### Preprocess the dataset

```bash
python preprocess.py
```

### Train the Linear Regression model

```bash
python train.py
```

This generates the trained model, label encoders, model metrics, and the Actual vs Predicted graph.

### Run the Streamlit application

```bash
streamlit run app.py
```

The application will open in your browser. On first launch, `meditrak.db` is created automatically — sign up for an account, then log in to start generating predictions. Use the sidebar to navigate to the Dashboard, Prediction History, Inventory Alerts, and My Account pages.

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Matplotlib
* Joblib
* Plotly
* SQLite (built-in `sqlite3`) for accounts and prediction history

## Future Improvements

Possible future enhancements include:

* Next-month demand forecasting
* Additional regression models for comparison
* Real pharmacy sales data integration
* Advanced inventory optimization
* Role-based access (e.g. store manager vs. pharmacy staff)
* Exporting prediction history and alerts to CSV/PDF
* Email-based password reset
* Cloud deployment

## Disclaimer

The dataset used in this project is synthetically generated for educational and demonstration purposes. The predictions should not be used for real-world medical, pharmaceutical, or business decisions without validation using real-world data.

## Author

**Shreeraksha**
AI/ML Internship Project
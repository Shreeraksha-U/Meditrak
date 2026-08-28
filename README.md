# Meditrak – Medicine Demand Forecasting System

Meditrak is a machine learning-based medicine demand forecasting system designed to help pharmacies predict future medicine demand and support better inventory planning.

The application uses a **Linear Regression** model to predict the expected number of units sold based on factors such as the store, medicine, price, promotion status, holiday status, and calendar-related features.

## Problem Statement

Pharmacies need to maintain an appropriate level of inventory to avoid:

* Overstocking of medicines
* Stock shortages
* Unnecessary inventory costs
* Poor demand planning

Meditrak addresses this problem by predicting the expected demand for medicines based on historical synthetic sales data and relevant business factors.

## Features

* Predict future medicine demand
* Select pharmacy/store and medicine
* Select a future forecast date
* Consider promotion and holiday conditions
* Automatically extract calendar features
* Categorize predicted demand as Low, Moderate, High, or Very High
* Provide inventory recommendations
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
| --------------- | ------------ | --------------------------- |
| Below 40        | Low          | Maintain minimum inventory  |
| 40–89           | Moderate     | Maintain regular stock      |
| 90–139          | High         | Increase inventory          |
| 140 and above   | Very High    | Place a replenishment order |

## Application Interface

The Streamlit application allows the user to:

1. Select a pharmacy/store.
2. Select a medicine.
3. Select a future forecast date.
4. Specify whether a promotion is active.
5. Specify whether the selected date is a holiday.
6. Generate a predicted demand value.
7. View the demand category.
8. Receive an inventory recommendation.

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
├── requirements.txt
├── README.md
├── .gitignore
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
└── src/
    ├── generate_dataset.py
    ├── preprocess.py
    ├── train.py
    └── predict.py
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

## Running the Project

### Generate the synthetic dataset

```bash
python src/generate_dataset.py
```

### Preprocess the dataset

```bash
python src/preprocess.py
```

### Train the Linear Regression model

```bash
python src/train.py
```

This generates the trained model, label encoders, model metrics, and the Actual vs Predicted graph.

### Run the Streamlit application

```bash
streamlit run app.py
```

The application will open in your browser.

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Matplotlib
* Joblib
* Plotly

## Future Improvements

Possible future enhancements include:

* Next-month demand forecasting
* Additional regression models for comparison
* Database integration for storing prediction history
* User authentication
* Real pharmacy sales data integration
* Advanced inventory optimization
* Automated low-stock alerts
* Cloud deployment

## Disclaimer

The dataset used in this project is synthetically generated for educational and demonstration purposes. The predictions should not be used for real-world medical, pharmaceutical, or business decisions without validation using real-world data.

## Author

**Shreeraksha**
AI/ML Internship Project

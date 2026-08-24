import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

#10 pharmacy branches
stores = [
    "Apollo Pharmacy", "SmartMed Pharmacy", "HealthMart", "BMS Pharmacy", "City Medicals",
    "Clarkson's Pharma", "Chen Drugstore", "Claire Drughouse", "Sara Medicos", "Lakshya Medicals"
]

#Medicines
medicines = [
    ("M101", "Paracetamol", "Painkiller", 25),
    ("M102", "Crocin", "Painkiller", 35),
    ("M103", "Dolo 650", "Painkiller", 30),
    ("M104", "Vitamin C", "Vitamin", 120),
    ("M105", "ORS", "Hydration", 25),
    ("M106", "Insulin", "Diabetes", 550),
    ("M107", "Metformin", "Diabetes", 80),
    ("M108", "Amoxicillin", "Antibiotic", 180),
    ("M109", "Azithromycin", "Antibiotic", 220),
    ("M110", "Cetirizine", "Allergy", 40),
    ("M111", "Benadryl", "Cough", 90),
    ("M112", "Cough Syrup", "Cough", 140),
    ("M113", "Digene", "Antacid", 60),
    ("M114", "Pantoprazole", "Antacid", 110),
    ("M115", "Calcium Tablet", "Supplement", 250),
    ("M116", "Iron Tablet", "Supplement", 180),
    ("M117", "BP Tablet", "Cardiac", 320),
    ("M118", "Asthma Inhaler", "Respiratory", 450),
    ("M119", "Eye Drops", "Eye Care", 160),
    ("M120", "Hand Sanitizer", "Hygiene", 90)
]

#one year of sales
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

data = [] #Every generated sale will be added to this list.

for _ in range(5000):
    random_days = random.randint(0, (end_date - start_date).days)
    date = start_date + timedelta(days=random_days)
    store = random.choice(stores) #Pick a random store
    item_id, medicine, category, price = random.choice(medicines) #Pick a random medicine
    is_weekend = 1 if date.weekday() >= 5 else 0 #Check whether it's a weekend
    holiday = 1 if random.random() < 0.10 else 0 #assume around 10% of days are holidays
    promotion = 1 if random.random() < 0.30 else 0 #Generate promotions, about 30% of sales happen during promotions.

    base_sales = 80
    if promotion:
        base_sales += 20

    if holiday:
        base_sales += 15

    if is_weekend:
        base_sales += 10

    base_sales -= price / 20

    base_sales += random.randint(-15, 15)

    units_sold = max(5, int(base_sales))

    data.append({
    "Date": date.strftime("%Y-%m-%d"),
    "Store_ID": store,
    "Item_ID": item_id,
    "Medicine_Name": medicine,
    "Category": category,
    "Base_Price": price,
    "Promotion": promotion,
    "Holiday": holiday,
    "Units_Sold": units_sold
    })
df = pd.DataFrame(data)
df.to_csv("dataset/medicine_sales.csv", index=False)

print("Dataset created successfully!")
print(df.head())
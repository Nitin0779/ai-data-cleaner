"""
Generate sample datasets for DataCleaner AI.
Run once: python generate_samples.py
"""
import pandas as pd
import numpy as np
import os

np.random.seed(42)
out_dir = os.path.join(os.path.dirname(__file__), "assets", "sample_datasets")
os.makedirs(out_dir, exist_ok=True)


# ── TITANIC ────────────────────────────────────────────────────────────
n = 891
age_vals = np.clip(np.random.normal(29.7, 14, n), 0.5, 80).astype(float)
age_mask = np.random.random(n) > 0.20
age_col  = np.where(age_mask, age_vals, np.nan)

fare_vals = np.clip(np.random.exponential(32, n), 0, 512)
fare_mask = np.random.random(n) > 0.001
fare_col  = np.where(fare_mask, fare_vals, np.nan)

cabin_choices = [f"{np.random.choice(['A','B','C','D','E'])}{np.random.randint(10,99)}" for _ in range(n)]
cabin_mask    = np.random.random(n) > 0.77
cabin_col     = [c if m else None for c, m in zip(cabin_choices, cabin_mask)]

emb_choices = np.random.choice(["S","C","Q"], n, p=[0.72,0.19,0.09]).tolist()
emb_mask    = np.random.random(n) > 0.02
emb_col     = [e if m else None for e, m in zip(emb_choices, emb_mask)]

titanic = pd.DataFrame({
    "PassengerId": range(1, n + 1),
    "Survived":    np.random.randint(0, 2, n),
    "Pclass":      np.random.choice([1, 2, 3], n, p=[0.24, 0.21, 0.55]),
    "Name":        [f"Passenger_{i}" for i in range(n)],
    "Sex":         np.random.choice(["male", "female"], n, p=[0.65, 0.35]),
    "Age":         age_col,
    "SibSp":       np.random.choice([0,1,2,3,4,5], n, p=[0.68,0.23,0.06,0.02,0.007,0.003]),
    "Parch":       np.random.choice([0,1,2,3,4], n, p=[0.76,0.13,0.08,0.02,0.01]),
    "Ticket":      [f"PC{np.random.randint(10000,99999)}" for _ in range(n)],
    "Fare":        fare_col,
    "Cabin":       cabin_col,
    "Embarked":    emb_col,
})
titanic.to_csv(os.path.join(out_dir, "titanic.csv"), index=False)
print("✅ titanic.csv created")


# ── HOUSE PRICES ───────────────────────────────────────────────────────
n = 1000
neighborhoods = ["NoRidge","NridgHt","StoneBr","Timber","Veenker","Somerst","Crawfor"]

lot_f_vals = np.clip(np.random.normal(70, 24, n), 21, 313)
lot_f_col  = np.where(np.random.random(n) > 0.18, lot_f_vals, np.nan)

gar_vals = np.clip(np.random.normal(473, 214, n).astype(int), 0, 1418).astype(float)
gar_col  = np.where(np.random.random(n) > 0.055, gar_vals, np.nan)

bsmt_vals = np.clip(np.random.normal(1057, 439, n).astype(int), 0, 6110).astype(float)
bsmt_col  = np.where(np.random.random(n) > 0.025, bsmt_vals, np.nan)

gar_type_choices = np.random.choice(["Attchd","Detchd","BuiltIn","CarPort","None"], n,
                                     p=[0.60,0.26,0.09,0.02,0.03]).tolist()
gar_type_col = [g if m else None for g, m in zip(gar_type_choices, np.random.random(n) > 0.055)]

house = pd.DataFrame({
    "Id":            range(1, n + 1),
    "LotArea":       np.random.randint(1500, 215245, n),
    "LotFrontage":   lot_f_col,
    "YearBuilt":     np.random.randint(1872, 2010, n),
    "YearRemodAdd":  np.random.randint(1950, 2010, n),
    "OverallQual":   np.random.randint(1, 11, n),
    "OverallCond":   np.random.randint(1, 10, n),
    "GrLivArea":     np.clip(np.random.normal(1515, 525, n).astype(int), 334, 5642),
    "BedroomAbvGr":  np.random.choice([0,1,2,3,4,5,6,7,8], n,
                                       p=[0.003,0.02,0.21,0.49,0.22,0.045,0.01,0.001,0.001]),
    "FullBath":      np.random.choice([0,1,2,3], n, p=[0.006,0.36,0.56,0.074]),
    "GarageArea":    gar_col,
    "TotalBsmtSF":   bsmt_col,
    "Neighborhood":  np.random.choice(neighborhoods, n),
    "BldgType":      np.random.choice(["1Fam","2fmCon","Duplex","TwnhsE","Twnhs"], n,
                                       p=[0.83,0.03,0.04,0.07,0.03]),
    "HouseStyle":    np.random.choice(["1Story","2Story","1.5Fin","SLvl","SFoyer"], n,
                                       p=[0.50,0.30,0.11,0.07,0.02]),
    "GarageType":    gar_type_col,
    "SalePrice":     np.clip(np.random.lognormal(np.log(180921), 0.4, n), 34900, 755000).astype(int),
})
house.to_csv(os.path.join(out_dir, "house_prices.csv"), index=False)
print("✅ house_prices.csv created")


# ── MALL CUSTOMERS ─────────────────────────────────────────────────────
n = 200
mall = pd.DataFrame({
    "CustomerID":         range(1, n + 1),
    "Genre":              np.random.choice(["Male", "Female"], n, p=[0.44, 0.56]),
    "Age":                np.random.randint(18, 70, n),
    "Annual Income (k$)": np.random.randint(15, 137, n),
    "Spending Score (1-100)": np.random.randint(1, 100, n),
})
mall.to_csv(os.path.join(out_dir, "mall_customers.csv"), index=False)
print("✅ mall_customers.csv created")


# ── CUSTOMER CHURN ─────────────────────────────────────────────────────
n = 500
monthly_vals = np.clip(np.random.normal(64.8, 30.1, n), 18.25, 118.75)
monthly_col  = np.where(np.random.random(n) > 0.005, monthly_vals, np.nan)

total_vals = np.clip(np.random.normal(2279, 2266, n), 18.8, 8684.8)
total_col  = np.where(np.random.random(n) > 0.011, total_vals, np.nan)

churn = pd.DataFrame({
    "CustomerID":      range(1, n + 1),
    "Gender":          np.random.choice(["Male", "Female"], n),
    "SeniorCitizen":   np.random.choice([0, 1], n, p=[0.84, 0.16]),
    "Partner":         np.random.choice(["Yes", "No"], n, p=[0.48, 0.52]),
    "Dependents":      np.random.choice(["Yes", "No"], n, p=[0.30, 0.70]),
    "Tenure":          np.random.randint(0, 72, n),
    "PhoneService":    np.random.choice(["Yes", "No"], n, p=[0.90, 0.10]),
    "InternetService": np.random.choice(["DSL","Fiber optic","No"], n, p=[0.34,0.44,0.22]),
    "Contract":        np.random.choice(["Month-to-month","One year","Two year"], n,
                                         p=[0.55, 0.21, 0.24]),
    "PaperlessBilling":np.random.choice(["Yes", "No"], n, p=[0.59, 0.41]),
    "PaymentMethod":   np.random.choice(
        ["Electronic check","Mailed check","Bank transfer","Credit card"], n,
        p=[0.34, 0.23, 0.22, 0.21]),
    "MonthlyCharges":  monthly_col,
    "TotalCharges":    total_col,
    "Churn":           np.random.choice(["Yes", "No"], n, p=[0.265, 0.735]),
})
churn.to_csv(os.path.join(out_dir, "customer_churn.csv"), index=False)
print("✅ customer_churn.csv created")

print("\n🎉 All sample datasets generated successfully!")
print(f"📁 Saved to: {out_dir}")

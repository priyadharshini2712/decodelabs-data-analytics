import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# PROJECT 2: EXPLORATORY DATA ANALYSIS (EDA)
# DecodeLabs Industrial Training | Batch 2026
# Dataset: Dataset_for_Data_Analytics.xlsx
# ============================================================

# Load clean data from Project 1
df = pd.read_csv('DecodeLabs_Clean_Data.csv')
df['Date'] = pd.to_datetime(df['Date'])

# STEP 1: DESCRIPTIVE STATISTICS
print("STEP 1: DESCRIPTIVE STATISTICS")
print(df[['Quantity','UnitPrice','TotalPrice','ItemsInCart']].describe().round(2))
print(f"\nTotal Revenue: {df['TotalPrice'].sum():,.2f}")
print(f"Avg Order Value: {df['TotalPrice'].mean():,.2f}")
print(f"Median Order Value: {df['TotalPrice'].median():,.2f}")

# STEP 2: DISTRIBUTION (Skewness)
print("\nSTEP 2: DISTRIBUTION ANALYSIS")
for col in ['Quantity','UnitPrice','TotalPrice','ItemsInCart']:
    print(f"{col}: Skew={df[col].skew():.2f}")

# STEP 3: OUTLIER DETECTION - IQR
print("\nSTEP 3: OUTLIER DETECTION")
for col in ['TotalPrice','UnitPrice','Quantity']:
    Q1=df[col].quantile(0.25); Q3=df[col].quantile(0.75); IQR=Q3-Q1
    out = df[(df[col]<Q1-1.5*IQR)|(df[col]>Q3+1.5*IQR)]
    print(f"{col}: {len(out)} outliers")

# STEP 4: TREND ANALYSIS
print("\nSTEP 4: TREND ANALYSIS")
print(df.groupby('Product')['TotalPrice'].sum().sort_values(ascending=False))
print(df['OrderStatus'].value_counts())
print(df['PaymentMethod'].value_counts())
print(df['ReferralSource'].value_counts())

# STEP 5: CORRELATION
print("\nSTEP 5: CORRELATION")
print(df[['Quantity','UnitPrice','TotalPrice','ItemsInCart']].corr().round(2))

# STEP 6: FIVE NUMBER SUMMARY
print("\nSTEP 6: FIVE NUMBER SUMMARY")
for col in ['TotalPrice','UnitPrice','Quantity']:
    print(f"\n{col}:")
    print(f"  Min={df[col].min():.2f} | Q1={df[col].quantile(0.25):.2f} | "
          f"Median={df[col].median():.2f} | Q3={df[col].quantile(0.75):.2f} | Max={df[col].max():.2f}")

print("\n✅ PROJECT 2 EDA COMPLETE!")

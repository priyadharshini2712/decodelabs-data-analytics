import pandas as pd
import numpy as np

# ============================================================
# PROJECT 1: DATA CLEANING & PREPARATION
# DecodeLabs Industrial Training | Batch 2026
# ============================================================

# --- LOAD RAW DATA ---
df = pd.read_csv('raw_dirty_data.csv')
print("=== ORIGINAL DIRTY DATA ===")
print(df.to_string())
print(f"\nShape: {df.shape}")

# ============================================================
# PHASE 1: STRATEGIC IMPUTATION (Handle Missing Values)
# ============================================================
print("\n=== MISSING VALUES BEFORE ===")
print(df.isnull().sum())

# Drop rows where Order_ID is missing (it's the primary key)
df = df.dropna(subset=['Order_ID'])

# Fill numeric columns with MEDIAN
df['Qty'] = df['Qty'].fillna(df['Qty'].median())
df['Value'] = df['Value'].fillna(round(df['Value'].median(), 2))

# Fill text columns with MODE
df['Product'] = df['Product'].fillna(df['Product'].mode()[0])

print("\n✅ PHASE 1 DONE: Missing values handled using Median/Mode imputation.")

# ============================================================
# PHASE 2: INTEGRITY AUDIT (Remove Duplicates)
# ============================================================
print("\n=== DUPLICATES FOUND ===")
print(df[df.duplicated(subset='Order_ID', keep=False)])

# Remove duplicates - keep first occurrence
before = len(df)
df = df.drop_duplicates(subset='Order_ID', keep='first')
after = len(df)

print(f"\n✅ PHASE 2 DONE: Removed {before - after} duplicate(s).")
assert df['Order_ID'].duplicated().sum() == 0
print("✅ 0% Error Rate on Unique Identifiers - VERIFIED")

# ============================================================
# PHASE 3: SPEAK ONE LANGUAGE (Standardize Formats)
# ============================================================

# Fix Status - Proper Case
df['Status'] = df['Status'].str.strip().str.title()

# Fix Product - Proper Case
df['Product'] = df['Product'].str.strip().str.title()

# Fix City - Normalize all variants
city_map = {
    'Bangalore': 'Bengaluru',
    'Bangaluru': 'Bengaluru',
    'Bangai':    'Bengaluru',
    'Blor':      'Bengaluru',
    'Blore':     'Bengaluru',
    'BLR':       'Bengaluru',
    'MUMBAI':    'Mumbai',
    'mumbai':    'Mumbai',
}
df['City'] = df['City'].replace(city_map)

# Fix Numeric Precision
df['Value'] = df['Value'].round(2)
df['Qty'] = df['Qty'].astype(int)

# Fix Dates - Convert everything to ISO 8601 (YYYY-MM-DD)
def parse_date(val):
    try:
        return pd.to_datetime(val, dayfirst=False).strftime('%Y-%m-%d')
    except:
        return pd.NaT

df['Timestamp'] = df['Timestamp'].apply(parse_date)

# Flag bad dates
bad_dates = df['Timestamp'].isnull().sum()
if bad_dates > 0:
    print(f"\n⚠️  {bad_dates} unparseable date(s) flagged as NaT")
    df['Timestamp'] = df['Timestamp'].fillna('DATE-ERROR-CHECK')

print("\n✅ PHASE 3 DONE: Formats standardized.")

# ============================================================
# CHANGE LOG
# ============================================================
change_log = pd.DataFrame({
    'Change_ID': ['CR001', 'CR002', 'CR003', 'CR004', 'CR005', 'CR006'],
    'Description': [
        'Dropped rows with missing Order_ID (primary key)',
        'Imputed missing Qty using Median',
        'Imputed missing Value using Median',
        'Imputed missing Product using Mode',
        'Removed duplicate Order_IDs (kept first occurrence)',
        'Standardized City names, Status, Date to ISO 8601'
    ],
    'Impact': [
        'Removed 1 invalid record',
        'Preserved 3 records',
        'Preserved 3 records',
        'Preserved 2 records',
        'Eliminated 2 duplicate transactions',
        'Unified all text and date inconsistencies'
    ],
    'Status': ['Resolved'] * 6
})

# ============================================================
# FINAL VERIFICATION
# ============================================================
print("\n=== FINAL CLEAN DATA ===")
print(df.to_string())
print(f"\nFinal Shape: {df.shape}")
print(f"\nDuplicate IDs: {df['Order_ID'].duplicated().sum()} ✅")
print(f"Missing Values:\n{df.isnull().sum()}")
print(f"Unique Cities: {sorted(df['City'].unique())}")
print(f"\n=== CHANGE LOG ===")
print(change_log.to_string(index=False))

# ============================================================
# EXPORT FILES
# ============================================================
df.to_csv('clean_data.csv', index=False)
change_log.to_csv('change_log.csv', index=False)
print("\n✅ Files saved: clean_data.csv | change_log.csv")

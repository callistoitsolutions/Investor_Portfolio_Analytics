import pandas as pd
from sqlalchemy import create_engine
import sys
import os

# -------------------------------
# Make project root discoverable
# -------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# -------------------------------
# Import DB credentials
# -------------------------------
try:
    from config.db_config import CONNECTION_STRING
except ImportError as e:
    print("Error importing DB credentials from config.db_config")
    print(e)
    sys.exit(1)

# -------------------------------
# Step 1: Load Excel file
# -------------------------------
excel_file = os.path.join(PROJECT_ROOT, "data", "raw", "Indian_Investor_Portfolio_4000.xlsx")
df = pd.read_excel(excel_file)

# -------------------------------
# Step 2: Clean column names
# -------------------------------
df.columns = (
    df.columns.str.strip()
              .str.replace('\n','', regex=False)
              .str.replace('\r','', regex=False)
              .str.replace('  ',' ', regex=False)
              .str.replace(' ','_', regex=False)
)
print("Cleaned Excel columns:", df.columns.tolist())

# -------------------------------
# Step 3: Map Excel columns to SQL columns
# -------------------------------
# Map Excel columns (left) to MySQL table columns (right)
investor_cols_mapping = {
    'Client_ID': 'client_id',
    'Client_Name': 'client_name',
    'Age': 'age',
    'Gender': 'gender',
    'City': 'city',
    'State': 'state'
}

investment_cols_mapping = {
    'Client_ID': 'client_id',
    'Asset_Type': 'asset_type',
    'Investment_Amount_INR': 'investment_amount',
    'Annual_Return_INR': 'annual_return_amount',
    'Investment_Start_Date': 'investment_start_date',
    'Investment_End_Date': 'investment_end_date'
}

# -------------------------------
# Step 4: Prepare DataFrames
# -------------------------------
# Investors table
investors = df[list(investor_cols_mapping.keys())].drop_duplicates()
investors = investors.rename(columns=investor_cols_mapping)

# Investments table
investments = df[list(investment_cols_mapping.keys())].copy()
investments = investments.rename(columns=investment_cols_mapping)

# -------------------------------
# Step 5: Connect to MySQL
# -------------------------------
engine = create_engine(CONNECTION_STRING)

# -------------------------------
# Step 6: Insert into SQL
# -------------------------------
try:
    investors.to_sql('investors', engine, if_exists='append', index=False)
    print(f"Inserted {len(investors)} investors.")
except Exception as e:
    print("Error inserting investors into SQL:")
    print(e)
    sys.exit(1)

try:
    investments.to_sql('portfolio_investments', engine, if_exists='append', index=False)
    print(f"Inserted {len(investments)} investments.")
except Exception as e:
    print("Error inserting investments into SQL:")
    print(e)
    sys.exit(1)

print("Data inserted successfully!")

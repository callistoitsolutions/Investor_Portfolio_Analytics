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
    from config.db_config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
except ImportError as e:
    print("Error importing DB credentials from config.db_config")
    print(e)
    sys.exit(1)

# -------------------------------
# Build SQLAlchemy connection string for MySQL
# -------------------------------
# Make sure you have 'pymysql' installed: pip install pymysql
CONNECTION_STRING = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# -------------------------------
# Create SQLAlchemy engine
# -------------------------------
engine = create_engine(CONNECTION_STRING)

# -------------------------------
# Load data function
# -------------------------------
def load_portfolio_data():
    query = "SELECT * FROM vw_portfolio_analysis"
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print("Error loading data from database:")
        print(e)
        sys.exit(1)

# -------------------------------
# Main script execution
# -------------------------------
if __name__ == "__main__":
    df = load_portfolio_data()
    
    # Ensure output folder exists
    output_folder = os.path.join(PROJECT_ROOT, "data", "processed")
    os.makedirs(output_folder, exist_ok=True)
    
    output_file = os.path.join(output_folder, "portfolio_data.csv")
    df.to_csv(output_file, index=False)
    print(f"Loaded {len(df)} records and saved to {output_file}")

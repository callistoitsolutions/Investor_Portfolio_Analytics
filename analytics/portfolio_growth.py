import pandas as pd
import numpy as np
import sys
import os

# -------------------------------
# Fix Python Path
# -------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from analytics.data_loader import load_portfolio_data
from analytics.roi_calculation import calculate_roi
from analytics.risk_analysis import calculate_risk

# -------------------------------
# Function: Portfolio Growth (CAGR)
# -------------------------------
def calculate_growth(df):
    """
    Calculates CAGR-based portfolio growth
    """

    # Convert to datetime
    df['investment_start_date'] = pd.to_datetime(df['investment_start_date'])
    df['investment_end_date'] = pd.to_datetime(df['investment_end_date'])

    # Calculate years invested
    df['years_invested'] = (
        (df['investment_end_date'] - df['investment_start_date'])
        .dt.days / 365
    )

    # Remove invalid durations
    df = df[df['years_invested'] > 0]

    # Ending value
    df['ending_value'] = (
        df['investment_amount'] + df['annual_return_amount']
    )

    # CAGR calculation
    df['cagr_percent'] = (
        (df['ending_value'] / df['investment_amount']) **
        (1 / df['years_invested']) - 1
    ) * 100

    return df

# -------------------------------
# Script Execution
# -------------------------------
if __name__ == "__main__":

    df = load_portfolio_data()

    # Apply analytics in correct order
    df = calculate_roi(df)
    df = calculate_risk(df)
    df = calculate_growth(df)

    # Save output
    output_path = os.path.join(
        PROJECT_ROOT, "data", "processed", "portfolio_growth.csv"
    )
    df.to_csv(output_path, index=False)

    print("✅ Portfolio growth analysis completed")
    print("📁 Saved:", output_path)
    print("\nSample CAGR output:")
    print(df[['client_id', 'asset_type', 'cagr_percent']].head())

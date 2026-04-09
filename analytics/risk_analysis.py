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

# -------------------------------
# Function: Hybrid Risk Calculation
# -------------------------------
def calculate_risk(df):
    """
    Hybrid Risk Model:
    - Asset type risk
    - ROI-based risk
    """

    # 1️⃣ Asset-based risk score
    asset_risk_map = {
        'Equity': 3,
        'Mutual Fund': 2,
        'ETF': 2,
        'Gold': 2,
        'Debt Fund': 1,
        'Fixed Deposit': 1
    }

    df['asset_risk_score'] = df['asset_type'].map(asset_risk_map).fillna(1)

    # 2️⃣ ROI-based risk score
    df['roi_risk_score'] = pd.cut(
        df['roi_percent'],
        bins=[-np.inf, 8, 15, np.inf],
        labels=[1, 2, 3]
    ).astype(int)

    # 3️⃣ Final weighted risk score
    df['risk_score'] = (
        df['asset_risk_score'] * 0.6 +
        df['roi_risk_score'] * 0.4
    )

    # 4️⃣ Risk level
    df['risk_level'] = pd.cut(
        df['risk_score'],
        bins=[0, 1.8, 2.4, np.inf],
        labels=['Low', 'Medium', 'High']
    )

    return df

# -------------------------------
# Script Execution
# -------------------------------
if __name__ == "__main__":

    # Load SQL data
    df = load_portfolio_data()

    # Always calculate ROI first
    df = calculate_roi(df)

    # Calculate risk
    df = calculate_risk(df)

    # Save output
    output_path = os.path.join(
        PROJECT_ROOT, "data", "processed", "portfolio_risk.csv"
    )
    df.to_csv(output_path, index=False)

    print("✅ Risk analysis completed successfully")
    print("📁 Saved:", output_path)
    print("\nRisk level distribution:")
    print(df['risk_level'].value_counts())

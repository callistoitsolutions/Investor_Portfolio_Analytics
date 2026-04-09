import pandas as pd
import numpy as np
from analytics.data_loader import load_portfolio_data
import os

def calculate_roi(df):
    # Calculate ROI %
    df['roi_percent'] = (df['annual_return_amount'] / df['investment_amount']) * 100
    # Total invested per client
    df['total_invested'] = df.groupby('client_id')['investment_amount'].transform('sum')
    return df

if __name__ == "__main__":
    df = load_portfolio_data()
    
    if df.empty:
        print("No portfolio data found in the database!")
    else:
        df = calculate_roi(df)
        
        # Display first few rows
        print(df[['client_id', 'asset_type', 'investment_amount', 'annual_return_amount', 'roi_percent']].head())
        
        # Save processed ROI
        output_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, "roi_data.csv")
        df.to_csv(output_file, index=False)
        print(f"ROI data saved to {output_file}")

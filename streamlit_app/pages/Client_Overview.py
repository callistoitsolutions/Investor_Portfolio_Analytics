import streamlit as st
from analytics.data_loader import load_portfolio_data
import analytics.roi_calculation as roi
import analytics.risk_analysis as risk
import analytics.portfolio_growth as growth

# ------------------------------
# Load data
# ------------------------------
df = load_portfolio_data()

# Normalize column names
df.columns = [c.lower() for c in df.columns]

# Sidebar client selector
clients = df['client_id'].unique()
selected_client = st.sidebar.selectbox("Select Client", clients)

client_df = df[df['client_id'] == selected_client]

# Apply calculations
client_df = roi.calculate_roi(client_df)
client_df = risk.calculate_risk(client_df)
client_df = growth.calculate_growth(client_df)

# ------------------------------
# Display KPIs
# ------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Assets", len(client_df))
col2.metric("Avg Age", round(client_df['age'].mean(), 1))
col3.metric("Top Asset", client_df['asset_type'].mode()[0])

st.subheader("Portfolio Details")
st.dataframe(client_df[['asset_type', 'investment_amount', 'roi_percent', 'risk_level']])

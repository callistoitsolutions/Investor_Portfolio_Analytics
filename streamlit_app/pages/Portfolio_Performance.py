import streamlit as st
import plotly.express as px
from analytics.data_loader import load_portfolio_data
import analytics.roi_calculation as roi
import analytics.risk_analysis as risk
import analytics.portfolio_growth as growth

# -----------------------------
# Initialize session state
# -----------------------------
if 'df' not in st.session_state:
    st.session_state['df'] = load_portfolio_data()

df = st.session_state['df']

# Default client selection
if 'selected_client' not in st.session_state:
    st.session_state['selected_client'] = df['client_id'].iloc[0]

selected_client = st.session_state['selected_client']

# -----------------------------
# Filter data for selected client
# -----------------------------
client_df = df[df['client_id'] == selected_client].copy()

# -----------------------------
# Apply calculations
# -----------------------------
client_df = roi.calculate_roi(client_df)
client_df = risk.calculate_risk(client_df)
client_df = growth.calculate_growth(client_df)  # Adds 'ending_value' & 'cagr_percent'

# -----------------------------
# Charts
# -----------------------------
# Use 'ending_value' or 'cagr_percent' instead of portfolio_growth_rate
fig_growth = px.line(
    client_df, 
    x='investment_start_date', 
    y='ending_value',  # <- Changed
    title=f"Portfolio Growth for {selected_client}",
    labels={'ending_value': 'Portfolio Value (₹)'}
)
st.plotly_chart(fig_growth, use_container_width=True)

fig_roi = px.bar(
    client_df, 
    x='asset_type', 
    y='roi_percent', 
    title=f"Asset ROI for {selected_client}",
    labels={'roi_percent': 'ROI (%)'}
)
st.plotly_chart(fig_roi, use_container_width=True)

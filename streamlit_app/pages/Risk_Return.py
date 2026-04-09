import streamlit as st
import plotly.express as px
from analytics.data_loader import load_portfolio_data
import analytics.roi_calculation as roi
import analytics.risk_analysis as risk
import analytics.portfolio_growth as growth

# -----------------------------
# Ensure the portfolio data is loaded in session_state
# -----------------------------
if 'df' not in st.session_state:
    st.session_state['df'] = load_portfolio_data()

df = st.session_state['df']

# -----------------------------
# Default client selection
# -----------------------------
if 'selected_client' not in st.session_state:
    st.session_state['selected_client'] = df['client_id'].iloc[0]

selected_client = st.session_state['selected_client']

# -----------------------------
# Filter data for the selected client
# -----------------------------
client_df = df[df['client_id'] == selected_client].copy()

# -----------------------------
# Run calculations
# -----------------------------
client_df = roi.calculate_roi(client_df)
client_df = risk.calculate_risk(client_df)
client_df = growth.calculate_growth(client_df)

# -----------------------------
# Plot Risk vs Return
# -----------------------------
fig_scatter = px.scatter(
    client_df,
    x='risk_score',
    y='roi_percent',
    color='risk_level',
    size='investment_amount',
    title=f"Risk vs Return for {selected_client}",
    labels={'risk_score': 'Risk Score', 'roi_percent': 'ROI (%)'}
)

st.plotly_chart(fig_scatter, use_container_width=True)

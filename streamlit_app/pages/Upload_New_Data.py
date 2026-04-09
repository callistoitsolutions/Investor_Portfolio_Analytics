import streamlit as st
import pandas as pd
import sys
import os
from sqlalchemy import create_engine

# Fix Python Path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from config.db_config import CONNECTION_STRING

st.title("📤 Upload New Investor Data")

uploaded_file = st.file_uploader("Upload new Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Read Excel
        new_df = pd.read_excel(uploaded_file)
        st.success(f"✅ Data uploaded successfully! {len(new_df)} rows")
        
        st.subheader("📋 Data Preview")
        st.dataframe(new_df.head(10))
        
        # **PROCESS BUTTON - FIXED!**
        if st.button("💾 **Process & Insert**", type="primary"):
            with st.spinner("🔄 Inserting to MySQL..."):
                engine = create_engine(CONNECTION_STRING)
                
                # **SIMPLE INSERT - NO VIEW DROP**
                new_df.to_sql("portfolio_data", engine, if_exists="append", index=False)
                
                st.success("🎉 **Data inserted successfully!**")
                st.success("✅ Refresh Streamlit & Power BI to see new data!")
                st.balloons()

    except Exception as e:
        st.error(f"❌ Upload failed: {e}")

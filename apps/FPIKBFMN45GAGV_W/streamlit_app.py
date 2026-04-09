import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import plotly.express as px

# 1. Setup & Branding
st.set_page_config(layout="wide", page_title="WA State EV Executive Insights")
session = get_active_session()

st.title("🚗 EV Population Strategy Dashboard")
st.caption("Powered by Snowflake Cortex & Open Iceberg Architecture")

# --- SECTION 1: EXECUTIVE INSIGHTS (Visuals) ---
st.header("Executive Insights")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Manufacturer Market Share")
    # Logic: Tesla vs. Others
    df_share = session.sql("""
        SELECT 
            CASE WHEN MAKE = 'TESLA' THEN 'Tesla' ELSE 'Other Manufacturers' END as CATEGORY,
            COUNT(*) as REGISTRATIONS
        FROM GOLD.VW_GOVERNED_EV_REGISTRATIONS
        GROUP BY 1
    """).to_pandas()
    fig1 = px.pie(df_share, values='REGISTRATIONS', names='CATEGORY', hole=0.4, 
                  color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Market Penetration: BEV vs. PHEV")
    df_type = session.sql("""
        SELECT EV_TYPE, COUNT(*) as TOTAL 
        FROM GOLD.VW_GOVERNED_EV_REGISTRATIONS 
        GROUP BY 1
    """).to_pandas()
    fig2 = px.bar(df_type, x='EV_TYPE', y='TOTAL', color='EV_TYPE', 
                  labels={'TOTAL': 'Total Registrations', 'EV_TYPE': 'Vehicle Type'})
    st.plotly_chart(fig2, use_container_width=True)

# --- SECTION 2: CONVERSATIONAL AI (Cortex Analyst) ---
st.divider()
st.header("💬 Ask the Data")
st.info("Ask questions like: 'Which 5 counties have the highest average electric range?' or 'What is the BEV market share in King County?'")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Enter your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing Washington EV data..."):
            # Call Cortex Analyst
            # Note: Replace with your specific stage path
            try:
                # Using the Snowflake Cortex Analyst REST API wrapper
                # This is a conceptual representation of the Analyst call in SiS
                resp = session.call("snowflake.cortex.analyst_ask", 
                                    "@LANDING.METADATA_STAGE/ev_model.yaml", 
                                    prompt)
                
                # Assume resp returns a dictionary with 'text' or 'data'
                # For demo purposes, we display the generated SQL or the answer
                st.markdown(resp['message']['content'][0]['text'])
                if 'sql' in resp:
                    with st.expander("View Generated SQL"):
                        st.code(resp['sql'])
            except Exception as e:
                st.error(f"Error connecting to Cortex: {str(e)}")
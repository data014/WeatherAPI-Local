import streamlit as st
import pandas as pd
import os
from weather_code import process_meteorology, extract_precipitation

CSV_FILE_PATH = r"weather_data.csv"
PCP_FILE_PATH = r"Precipitations.csv"

# def to_excel(df):
#     output = io.BytesIO()
#     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#         df.to_excel(writer, index=False, sheet_name='Data')
#     return output.getvalue()

st.set_page_config(page_title="Powai Weather Data", layout="wide")
st.markdown(
    """
    <style>
    .title {
        font-size: 40px;
        color: #4B0082;
        text-align: center;
    }
    .subheader {
        font-size: 24px;
        color: #4B0082;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="title">Live Weather Data - Powai</div>', unsafe_allow_html=True)
st.divider()

# Load all data
df = pd.read_csv(CSV_FILE_PATH)
df = df.sort_values(by='Timestamp', ascending=False)
df = df.reset_index(drop=True)
dfp = pd.read_csv(PCP_FILE_PATH) 

# Placeholder-1
st.subheader("Precipitation Data (24 hours forecast)")
precipitation_placeholder = st.empty()
with precipitation_placeholder:
    st.dataframe(dfp, use_container_width=True)
st.divider()

# Placeholder-2
st.subheader("Weather Data (past+current)")
weather_placeholder = st.empty()
with weather_placeholder:
    st.dataframe(df, use_container_width=True) 
    
# process start in infinite-loop
process_meteorology()

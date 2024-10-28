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

# Custom CSS for styling
st.set_page_config(page_title="Weather Data Viewer", layout="wide")
st.markdown(
    """
    <style>
    .title {
        font-size: 40px;
        color: #4B0082;
        text-align: center;
    }
    .header {
        font-size: 24px;
        color: #4B0082;
        text-align: center;
        margin-bottom: 20px;
    }
    .button {
        background-color: #4B0082; 
        color: white; 
        border-radius: 10px; 
        padding: 10px 20px; 
        font-size: 16px;
    }
    .button:hover {
        background-color: #6A0DAD;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title">Live Weather Data - Powai</div>', unsafe_allow_html=True)
st.divider()
st.write(f"Displaying live data from: **{os.path.basename(CSV_FILE_PATH)}**")

# Load main weather data
df = pd.read_csv(CSV_FILE_PATH)
dfp = pd.read_csv(PCP_FILE_PATH) 

# Placeholder-1
precipitation_placeholder = st.empty()
with precipitation_placeholder:
    st.header("Precipitation Data")
    st.dataframe(dfp, use_container_width=True)
st.divider()
# Placeholder-2
weather_placeholder = st.empty()
with weather_placeholder:
    st.header("Weather Data")
    st.dataframe(df, use_container_width=True) 
    
# process start in infinite-loop
process_meteorology()

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
col1 = [
    "Date", "Time", "Location", "Temperature", "Weather Type", "AQI",
    "Description", "Feels Like", "Day", "Night", "Sunrise", "Sunset", "High",
    "Low", "Wind (km/h)", "Humidity", "Dew Point", "Pressure (mb)",
    "UV Index", "Visibility (km)", "Moon Phase"
]
df = df[col1]
df = df.sort_values(by=["Date","Time"], ascending=False)
df = df.reset_index(drop=True)

dfp = pd.read_csv(PCP_FILE_PATH) 
col2 = [
    "Date", "Time", "Temperature", "Feels Like", "Weather", 
    "Rain Chance (%)", "Wind Direction", "Wind Speed (km)", 
    "Humidity (%)", "UV Index", "Rain Amount (mm)"
]
dfp = dfp[col2]

# Placeholder-1
st.subheader("Weather Data (past+current)")
weather_placeholder = st.empty()
with weather_placeholder:
    st.dataframe(df, use_container_width=True) 
    
# Placeholder-2
st.subheader("Precipitation Data (24 hours forecast)")
precipitation_placeholder = st.empty()
with precipitation_placeholder:
    st.dataframe(dfp, use_container_width=True)
st.divider()

# process start in infinite-loop
process_meteorology()

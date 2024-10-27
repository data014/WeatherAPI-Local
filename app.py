import streamlit as st
import pandas as pd
import os
import io
from weather_code import process_meteorology

CSV_FILE_PATH = r"weather_data.csv"  

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    return output.getvalue()


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

st.markdown('<div class="title">Live Weather Data Viewer</div>', unsafe_allow_html=True)


if os.path.exists(CSV_FILE_PATH):
    st.write(f"Displaying live data from: **{os.path.basename(CSV_FILE_PATH)}**")

    data_placeholder = st.empty()

    # Display initial data
    df = pd.read_csv(CSV_FILE_PATH)
    with data_placeholder:
        st.dataframe(df, use_container_width=True)  # Display full data
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='weather_data.csv',
            mime='text/csv'
        )

        excel = to_excel(df)
        st.download_button(
            label="Download Excel",
            data=excel,
            file_name='weather_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    df = pd.read_csv(CSV_FILE_PATH) 
    with data_placeholder:
        st.dataframe(df, use_container_width=True) 
    # Set a refresh button to update data
    if st.button('Refresh Data'):
        process_meteorology()
        df = pd.read_csv(CSV_FILE_PATH)  # Reloads the updated file
        with data_placeholder:
            st.dataframe(df, use_container_width=True)  # Display updated data
else:
    st.write("The file 'weather_data.csv' does not exist in the specified path.")

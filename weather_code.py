import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from datetime import datetime
import os
import pytz

def append_to_csv(data, filename='weather_data.csv'):
    df = pd.DataFrame([data])  
    if os.path.exists(filename):
        existing_df = pd.read_csv(filename)  
        last_rows = existing_df.tail(20)
        condition = (
            (last_rows['Timestamp'] == df['Timestamp'].iloc[0]) |
            (last_rows['Time'] == df['Time'].iloc[0])
        )
        if condition.any():  # If any row matches the condition
            print("Skipping append....")
            return
    df.to_csv(filename, mode='a', header=not os.path.exists(filename), index=False)
    print(f"Data appended at {data['Timestamp']}")


def extract_precipitation():
    url = "https://weather.com/en-IN/weather/hourbyhour/l/1d7873a08fd263cfdf311f0c025cc1c1d3081de6381fc557c6ea312a872fc411"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    
    data = [] #dict for DF
    for k in range(24):
        try:
            element = soup.find(id=f'detailIndex{k}')
            summary_data = element.find("summary").get_text(strip=True, separator="\n").split("\n")
            time.sleep(2)
            ui_data = element.find("ul").get_text(strip=True, separator="\n").split("\n")
            rain_ch, feels, wind_dir, wind_spd, hum, uv_idx, rain_amt = [None] * 7
            for i in range(len(summary_data)):
                t=summary_data[0]
                if str(summary_data[i])=="Rain":
                    rain_ch=int(summary_data[i+1].replace('%',''))
                    break
            for i in range(len(ui_data)):
                if str(ui_data[i])=="Feels Like":
                    feels=ui_data[i+1]
                if str(ui_data[i])=="Wind":
                    wind_dir=ui_data[i+1]
                    wind_spd=ui_data[i+2]
                if str(ui_data[i])=="Humidity":
                    hum=ui_data[i+1].replace('%','')
                if str(ui_data[i])=="UV Index":
                    uv_idx=ui_data[i+1]
                if str(ui_data[i])=="Rain Amount":
                    rain_amt=ui_data[i+1]

            india_timezone = pytz.timezone('Asia/Kolkata')
            dt = datetime.now(india_timezone)
            dt = dt.strftime('%Y-%m-%d %H:%M:%S')

            print("PCP: ", dt,t,rain_ch,feels,wind_dir,wind_spd,hum,uv_idx,rain_amt)
            # Store to DF
            data.append({
                "Timestamp": dt,
                "Time": t,
                'Rain Chance (%)': rain_ch,
                'Feels Like': feels,
                'Wind Direction': wind_dir,
                'Wind Speed (km)': wind_spd,
                'Humidity (%)': hum,
                'UV Index': uv_idx,
                'Rain Amount (mm)': rain_amt
            })
        except Exception as e:
            print(f"Error processing detailIndex{k}: {e}")
    df = pd.DataFrame(data)
    df.to_csv("Precipitations.csv", index=False)
    print("LOG: Precipitations SAVED SUCCESSFULLY")

def extract_meteorology(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data1_elem = soup.find(id="WxuCurrentConditions-main-b3094163-ef75-4558-8d9a-e35e6b9b1034")
        data1 = data1_elem.get_text(separator="\n").split("\n") if data1_elem else []

        data2_elem = soup.find(id="todayDetails")
        data2 = data2_elem.get_text(separator="\n").split("\n") if data2_elem else []

        aqi_elem = soup.find(id="WxuAirQuality-sidebar-aa4a4fb6-4a9b-43be-9004-b14790f57d73")
        aqi_data = aqi_elem.get_text(separator="\n").split("\n")[1:3] if aqi_elem else []

        print(data1, data2, aqi_data)
        return data1, data2, aqi_data

    except requests.exceptions.RequestException as e:
        print(f"Error occurred during data extraction: {e}")
        return None, None, None


def get_data(url):
    try:
        data1, data2, aqi_data = extract_meteorology(url)
        
        if not data1 or not data2 or not aqi_data:
            print("LOG: One or more data elements are missing")
            return
        # Extract AQI and description safely
        aqi = int(aqi_data[0]) if aqi_data and aqi_data[0].isdigit() else None
        desc = aqi_data[1] if aqi_data and len(aqi_data) > 1 else None
        
        # Safely extract time, temperature, and weather type
        loc = data1[0].strip()
        t = re.search(r"(\d{2}:\d{2})", data1[1])
        temp = int(data1[2]) if data1[2].isdigit() else None
        weather_type = data1[4] if len(data1) > 4 else None
        day = data1[7] if len(data1) > 7 else None
        night = data1[14] if len(data1) > 14 else None

        # Extract meteorological data safely
        for i in range(len(data2)):
            if data2[i]=="Feels Like":
                feels_like = float(data2[i+1])
            if data2[i]=="Sun Rise":
                sunrise = data2[i+1]
            if data2[i]=="Sunset":
                sunset = data2[i+1]
            if data2[i]=="High/Low":
                high = data2[i+1]
                low = data2[i+3]
            if data2[i]=="Wind Direction":
                wind = float(data2[i+1])
            if data2[i]=="Humidity":
                humidity = data2[i+1]
                if data2[i+1]=="Humidity":
                    humidity = data2[i+2]
            if data2[i]=="Dew Point":
                dew = data2[i+1]
                if data2[i+1]=="Dew Point":
                    dew = data2[i+2]
            if data2[i]=="Pressure":
                pressure = data2[i+2]
                if isinstance(data2[i+1], (int, float)):
                    pressure = data2[i+1]
            if data2[i]=="UV Index":
                uv = data2[i+1]
            if data2[i]=="Visibility":
                visibility = data2[i+1]
                if data2[i+1]=="Visibility":
                    visibility = data2[i+2]
            if data2[i]=="Moon Phase":
                moon = str(data2[i+1]).strip()
        
        india_timezone = pytz.timezone('Asia/Kolkata')
        dt = datetime.now(india_timezone)
        dt = dt.strftime('%Y-%m-%d %H:%M:%S')
        new_row = {
            "Timestamp": dt,
            'Time': t.group(1) if t else None,
            'Location': loc,
            'Temperature': temp,
            'Weather Type': weather_type,
            'AQI': aqi,
            'Description': desc,
            'Feels Like': feels_like,
            'Day': day,
            'Night': night,
            'Sunrise': sunrise,
            'Sunset': sunset,
            'High': high,
            'Low': low,
            'Wind (km/h)': wind,
            'Humidity': humidity,
            'Dew Point': dew,
            'Pressure (mb)': pressure,
            'UV Index': uv,
            'Visibility (km)': visibility,
            'Moon Phase': moon
        }
        
        append_to_csv(new_row)

    except Exception as e:
        print(f"Exception occurred: {e}")

def process_meteorology():
    url = "https://weather.com/en-IN/weather/today/l/1d7873a08fd263cfdf311f0c025cc1c1d3081de6381fc557c6ea312a872fc411" #powai

    while True:
        try:
            get_data(url)
            extract_precipitation()
        except Exception as e:
            print(e)
        time.sleep(60)

# process_meteorology()
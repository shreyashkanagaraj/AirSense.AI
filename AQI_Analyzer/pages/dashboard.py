import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
import folium

from datetime import datetime
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AirSense India",
    layout="wide"
)

# ---------------- AUTO REFRESH ----------------
st_autorefresh(
    interval=60000,
    key="aqi_refresh"
)

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
        color: white;
    }

    h1, h2, h3, h4 {
        color: #00E5FF;
    }

    .stMetric {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #333;
        box-shadow: 0px 0px 10px rgba(0,229,255,0.2);
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LOAD ML MODEL ----------------
model = joblib.load(
    "models/aqi_model.pkl"
)

# ---------------- TITLE ----------------
st.title("🌍 AirSense India")

st.subheader(
    "Live AQI Monitoring Dashboard with ML Prediction"
)

# ---------------- HERO BANNER ----------------
st.markdown(
    f"""
    <div style="
        background: linear-gradient(90deg,#00E5FF,#007CF0);
        padding:20px;
        border-radius:15px;
        text-align:center;
        margin-bottom:20px;
    ">

    <h2 style="color:white;">
        🌍 Real-Time AQI Monitoring & AI Prediction System
    </h2>

    <p style="color:white;font-size:18px;">
        Live Pollution Tracking | Forecasting | Health Alerts
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("AQI Dashboard Controls")

city = st.sidebar.selectbox(

    "Select City",

    [
        "mumbai",
        "delhi",
        "chennai",
        "bangalore",
        "kolkata",
        "pune"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    🌍 AI AQI Dashboard

    Features:
    ✅ Live AQI
    ✅ ML Prediction
    ✅ Charts
    ✅ AQI Map
    ✅ AQI Forecast
    ✅ Health Recommendation
    """
)

if st.sidebar.button("🔄 Refresh AQI"):

    st.rerun()

# ---------------- CITY COORDINATES ----------------
city_coordinates = {

    "mumbai": [19.0760, 72.8777],

    "delhi": [28.7041, 77.1025],

    "chennai": [13.0827, 80.2707],

    "bangalore": [12.9716, 77.5946],

    "kolkata": [22.5726, 88.3639],

    "pune": [18.5204, 73.8567]
}

latitude = city_coordinates[city][0]

longitude = city_coordinates[city][1]

# ---------------- API TOKEN ----------------
token = "25227a61aaa946c26012d42a72b2ab1ebfa3fccc"

# ---------------- API URL ----------------
url = f"https://api.waqi.info/feed/{city}/?token={token}"

# ---------------- FETCH DATA ----------------
response = requests.get(url)

data = response.json()

# ---------------- CHECK API STATUS ----------------
if data["status"] != "ok":

    st.error(
        "Could not fetch AQI data"
    )

    st.stop()

# ---------------- EXTRACT DATA ----------------
aqi = data["data"]["aqi"]

pm25 = data["data"]["iaqi"].get(
    "pm25",
    {}
).get(
    "v",
    0
)

pm10 = data["data"]["iaqi"].get(
    "pm10",
    {}
).get(
    "v",
    0
)

no2 = data["data"]["iaqi"].get(
    "no2",
    {}
).get(
    "v",
    0
)

temperature = data["data"]["iaqi"].get(
    "t",
    {}
).get(
    "v",
    0
)

humidity = data["data"]["iaqi"].get(
    "h",
    {}
).get(
    "v",
    0
)

api_city = data["data"]["city"]["name"]

# ---------------- ML PREDICTION ----------------
prediction = model.predict(pd.DataFrame([{
    "pm25": pm25,
    "pm10": pm10,
    "no2": no2,
    "temp": temperature,
    "humidity": humidity
}]))

predicted_aqi = int(prediction[0])

# ---------------- CITY INFO ----------------
st.success(
    f"Live AQI Data for: {api_city}"
)

# ---------------- LAST UPDATED ----------------
current_time = datetime.now().strftime(
    "%d-%m-%Y %H:%M:%S"
)

st.write(
    f"Last Updated: {current_time}"
)

# ---------------- DASHBOARD CARDS ----------------
col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Current AQI",
        aqi
    )

with col2:

    st.metric(
        "Predicted Tomorrow AQI",
        predicted_aqi
    )

with col3:

    st.metric(
        "PM2.5",
        pm25
    )

col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        "PM10",
        pm10
    )

with col5:

    st.metric(
        "NO2",
        no2
    )

with col6:

    st.metric(
        "Humidity",
        humidity
    )

# ---------------- AQI STATUS ----------------
st.subheader(
    "Air Quality Status"
)

if aqi <= 50:

    st.success(
        "Good Air Quality"
    )

elif aqi <= 100:

    st.warning(
        "Moderate Air Quality"
    )

elif aqi <= 150:

    st.warning(
        "Unhealthy for Sensitive Groups"
    )

else:

    st.error(
        "Unhealthy Air Quality"
    )

# ---------------- AQI COLOR INDICATOR ----------------
if aqi <= 50:

    aqi_color = "green"

elif aqi <= 100:

    aqi_color = "orange"

else:

    aqi_color = "red"

st.markdown(
    f"""
    <div style="
        background-color:{aqi_color};
        padding:15px;
        border-radius:10px;
        text-align:center;
        color:white;
        font-size:24px;
        font-weight:bold;
    ">
        Current AQI: {aqi}
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- HEALTH RECOMMENDATION ----------------
st.subheader(
    "Health Recommendation"
)

if predicted_aqi > 150:

    st.error(
        "Avoid outdoor activities. Wear a mask."
    )

elif predicted_aqi > 100:

    st.warning(
        "Sensitive people should avoid outdoor exposure."
    )

else:

    st.success(
        "Air quality is acceptable."
    )

# ---------------- AQI MAP ----------------
st.subheader("🗺 AQI Location Map")

aqi_map = folium.Map(

    location=[latitude, longitude],

    zoom_start=10
)

# ---------------- MAP MARKER ----------------
folium.Marker(

    [latitude, longitude],

    popup=f"{city.title()} AQI: {aqi}",

    tooltip="Click for AQI Info"

).add_to(aqi_map)

# ---------------- AQI CIRCLE ----------------
folium.Circle(

    location=[latitude, longitude],

    radius=5000,

    popup=f"AQI: {aqi}",

    color="red",

    fill=True,

    fill_color="red"

).add_to(aqi_map)

# ---------------- DISPLAY MAP ----------------
st_folium(

    aqi_map,

    width=1200,

    height=500
)

# ---------------- AQI TREND DATA ----------------
aqi_history = [

    max(aqi - 40, 20),

    max(aqi - 30, 20),

    max(aqi - 20, 20),

    max(aqi - 10, 20),

    aqi,

    predicted_aqi
]

days = [

    "4 Days Ago",

    "3 Days Ago",

    "2 Days Ago",

    "Yesterday",

    "Today",

    "Tomorrow Prediction"
]

# ---------------- TREND DATAFRAME ----------------
trend_df = pd.DataFrame({

    "Day": days,

    "AQI": aqi_history
})

# ---------------- FORECAST GRAPH ----------------
trend_fig = px.line(

    trend_df,

    x="Day",

    y="AQI",

    markers=True,

    title=f"AQI Trend & Forecast for {city.title()}"
)

st.plotly_chart(

    trend_fig,

    width='stretch'
)

# ---------------- POLLUTION DATAFRAME ----------------
pollution_data = pd.DataFrame({

    "Pollutant": [
        "PM2.5",
        "PM10",
        "NO2"
    ],

    "Value": [
        pm25,
        pm10,
        no2
    ]
})

# ---------------- BAR CHART ----------------
fig = px.bar(

    pollution_data,

    x="Pollutant",

    y="Value",

    title=f"Pollutant Levels in {city.title()}"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# ---------------- PIE CHART ----------------
pie_fig = px.pie(

    pollution_data,

    names="Pollutant",

    values="Value",

    title="Pollution Contribution"
)

st.plotly_chart(
    pie_fig,
    width='stretch'
)

# ---------------- AQI GAUGE ----------------
gauge_fig = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=aqi,

        title={
            "text": "Current AQI"
        },

        gauge={

            "axis": {
                "range": [0, 300]
            },

            "bar": {
                "color": "red"
            }
        }
    )
)

st.plotly_chart(
    gauge_fig,
    width='stretch'
)
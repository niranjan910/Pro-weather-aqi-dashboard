# weather_dashboard.py

"""
Professional Weather & AQI Dashboard
Single-file version (config + utils + API service + app combined).
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json

# ================= CONFIG =================

DATA_FILE_PATH = r"E:\Data Science 2025\9. Python Project\1. Weather Forecast Project\Data\city.list.json"

API_KEY = "10b0b3741256c3d840ad164ba3cba2c8"  # <-- Your API key

BASE_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
BASE_AQI_URL = "http://api.openweathermap.org/data/2.5/air_pollution"


# ================= UTILS =================
@st.cache_data
def load_cities(file_path):
    """Load Indian cities from JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            cities_data = json.load(f)
        df = pd.DataFrame(cities_data)
        indian_cities_df = df[df["country"] == "IN"]
        return sorted(indian_cities_df["name"].unique())
    except FileNotFoundError:
        st.error(f"City data file not found at {file_path}")
        return []
    except json.JSONDecodeError:
        st.error("Error decoding city data JSON file.")
        return []


def get_aqi_description(aqi_value):
    """Return description & color for AQI level."""
    if aqi_value == 1:
        return "Good", "green"
    elif aqi_value == 2:
        return "Fair", "yellow"
    elif aqi_value == 3:
        return "Moderate", "orange"
    elif aqi_value == 4:
        return "Poor", "red"
    elif aqi_value == 5:
        return "Very Poor", "purple"
    else:
        return "Unknown", "gray"


# ================= API SERVICE =================
@st.cache_data(ttl=600)
def get_weather_data(city):
    """Fetch current weather + AQI for a city."""
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        weather_response = requests.get(BASE_WEATHER_URL, params=params)
        weather_response.raise_for_status()
        data = weather_response.json()

        lat, lon = data["coord"]["lat"], data["coord"]["lon"]

        # AQI fetch
        aqi_params = {"lat": lat, "lon": lon, "appid": API_KEY}
        aqi_response = requests.get(BASE_AQI_URL, params=aqi_params)
        aqi_response.raise_for_status()
        aqi_data = aqi_response.json()
        aqi = aqi_data["list"][0]["main"]["aqi"] if aqi_data["list"] else None

        return {
            "City": city,
            "Temperature": data["main"]["temp"],
            "Feels Like": data["main"]["feels_like"],
            "Humidity": data["main"]["humidity"],
            "Wind Speed": data["wind"]["speed"],
            "Description": data["weather"][0]["description"].title(),
            "AQI": aqi,
            "Latitude": lat,
            "Longitude": lon,
        }
    except Exception as e:
        st.error(f"Error fetching data for {city}: {e}")
        return None


@st.cache_data(ttl=600)
def get_forecast_data(lat, lon):
    """Fetch 5-day forecast for given coordinates."""
    params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_FORECAST_URL, params=params)
        response.raise_for_status()
        forecast_data = response.json()

        processed = []
        for item in forecast_data["list"]:
            processed.append(
                {
                    "Date": pd.to_datetime(item["dt_txt"]),
                    "Temperature": item["main"]["temp"],
                    "Description": item["weather"][0]["description"].title(),
                }
            )
        df = pd.DataFrame(processed)
        return (
            df.set_index("Date")
            .resample("D")["Temperature"]
            .agg(["min", "max"])
            .reset_index()
        )
    except Exception as e:
        st.error(f"Error fetching forecast data: {e}")
        return None


# ================= APP =================
st.set_page_config(
    page_title="Pro Weather & AQI Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🌦️ Professional Weather & AQI Dashboard")
st.markdown(
    "An interactive dashboard to analyze real-time weather and air quality for Indian cities."
)

# Sidebar
st.sidebar.header("📍 City Selection")
all_cities = load_cities(DATA_FILE_PATH)
if all_cities:
    selected_cities = st.sidebar.multiselect(
        "Select cities to compare:",
        options=all_cities,
        default=["Kolkata", "Mumbai", "Delhi", "Bengaluru"],
    )
else:
    selected_cities = []

# Main
if not selected_cities:
    st.info("Please select at least one city from the sidebar.")
else:
    with st.spinner("Fetching latest weather data..."):
        weather_data = [get_weather_data(city) for city in selected_cities]
        weather_data = [d for d in weather_data if d]

    if weather_data:
        df = pd.DataFrame(weather_data)

        # --- Map & Metrics ---
        st.subheader("📍 City Locations & Key Metrics")
        col1, col2 = st.columns([2, 1])

        with col1:
            st.map(
                df[["Latitude", "Longitude"]].rename(
                    columns={"Latitude": "lat", "Longitude": "lon"}
                )
            )

        with col2:
            for _, row in df.iterrows():
                aqi_desc, aqi_color = get_aqi_description(row["AQI"])
                st.markdown(
                    f"""
                    **{row['City']}**
                    - 🌡️ Temp: `{row['Temperature']}°C` (Feels like `{row['Feels Like']}°C`)
                    - 💧 Humidity: `{row['Humidity']}%`
                    - 💨 Wind: `{row['Wind Speed']} m/s`
                    - 🌫️ AQI: <span style='color:{aqi_color};'>{row['AQI']} ({aqi_desc})</span>
                    """,
                    unsafe_allow_html=True,
                )

        st.divider()

        # --- Comparative Charts ---
        st.subheader("📊 Comparative Analysis")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            fig_temp = px.bar(
                df,
                x="City",
                y="Temperature",
                text_auto=True,
                title="Temperature Comparison (°C)",
                color="Temperature",
                color_continuous_scale="reds",
            )
            st.plotly_chart(fig_temp, use_container_width=True)

        with chart_col2:
            fig_hum = px.bar(
                df,
                x="City",
                y="Humidity",
                text_auto=True,
                title="Humidity Comparison (%)",
                color="Humidity",
                color_continuous_scale="blues",
            )
            st.plotly_chart(fig_hum, use_container_width=True)

        st.divider()

        # --- Forecast ---
        st.subheader("🗓️ 5-Day Forecast")
        forecast_city = st.selectbox("Select a city:", df["City"].tolist())
        if forecast_city:
            city_info = df[df["City"] == forecast_city].iloc[0]
            forecast_df = get_forecast_data(
                city_info["Latitude"], city_info["Longitude"]
            )
            if forecast_df is not None:
                fig_forecast = px.line(
                    forecast_df,
                    x="Date",
                    y=["min", "max"],
                    markers=True,
                    title=f"5-Day Min/Max Temperature Forecast for {forecast_city}",
                    labels={"value": "Temperature (°C)", "variable": "Forecast"},
                )
                st.plotly_chart(fig_forecast, use_container_width=True)

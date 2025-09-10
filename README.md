# Weather Forecast Project 🌤️

## Project Overview
The **Weather Forecast Project** is a Python-based application that fetches real-time weather data for any city using the OpenWeatherMap API. The project demonstrates data extraction, cleaning, visualization, and deployment of a live web application.

This project showcases skills in:
- Python programming
- Data cleaning and preprocessing
- API integration
- Data visualization
- Deployment of a web application

---

## Project Live
The project is live and can be accessed here: [**Streamline Weather Forecast**](https://pro-weather-aqi-dashboard-xtbjpiv8uwftmnmznvambh.streamlit.app/)

---

## Features
- Fetch current weather data for any city worldwide.
- Display temperature, humidity, pressure, wind speed, and weather description.
- Clean and structured display of the data.
- Live updates via API integration.
- Simple, user-friendly interface.

---

## Data Source
- Weather data is collected from **[OpenWeatherMap API](https://openweathermap.org/current)**.
- API Key used: `10b0b3741256c3d840ad164ba3cba2c8`  
- Data collected includes:
  - Temperature
  - Humidity
  - Pressure
  - Wind Speed
  - Weather Condition

---

## Project Structure


---

## Steps Performed

### 1. Data Collection
- Collected city list from OpenWeatherMap JSON file: `city.list.json`.
- Used OpenWeatherMap API to fetch current weather data for selected cities.
- Stored data in structured format for analysis.

### 2. Data Cleaning
- Checked for missing values or corrupted entries.
- Removed duplicates if any.
- Standardized column names and formats.
- Converted temperature from Kelvin to Celsius for readability.

### 3. Data Analysis & Visualization
- Extracted important weather metrics:
  - Temperature
  - Humidity
  - Pressure
  - Wind Speed
- Visualized metrics using **Matplotlib** and **Seaborn**:
  - Temperature trends
  - Humidity comparison
  - Wind speed variations

### 4. Deployment
- Python Flask framework used to create a simple web interface.
- Hosted the application live on **Streamline** platform.
- User can input any city and get live weather updates instantly.

---

## Installation & Usage

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/weather-forecast-project.git
cd weather-forecast-project
```

2. **Install Dependencies** - pip install -r requirements.txt
3. **Run the Application** - python Scripts/weather_app.py
4. Acess the App
- Open your browser and go to : `http://localhost:5000`
- Enter any City to get the current weather details.
  
## Technologies Used
- Python 3.x – Programming language
- Jupyter Notebook – Data cleaning & exploration
- Flask – Web framework for deployment
- OpenWeatherMap API – Weather data source

## Learning and skills Gained
- Hands-on experience in API integration and data handling.
- Improved data cleaning and preprocessing techniques.
- Learned to deploy Python applications as live web apps.
- Developed data visualization skills for presenting insights.
- Strengthened problem-solving and project structuring skills for real-world applications.

## Github Contribution
- Project uploaded to github for portfolio shocase
- Proper directory structure and version control maintained.
- README written in a detailed, resume - redy format

## Author 
Niranjan 

## License 
This project is licensed under the MIT License. See LICENSE for details.

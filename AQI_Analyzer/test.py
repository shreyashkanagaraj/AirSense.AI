from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("AQI_TOKEN")

# API URL for Mumbai
url = f"https://api.waqi.info/feed/mumbai/?token={token}"

# Send request to API
response = requests.get(url)

# Convert response to JSON
data = response.json()

# Print full data
print(data)

# ---------------- EXTRACT VALUES ----------------

aqi = data["data"]["aqi"]

pm25 = data["data"]["iaqi"].get(
    "pm25",
    {}
).get(
    "v",
    "N/A"
)

pm10 = data["data"]["iaqi"].get(
    "pm10",
    {}
).get(
    "v",
    "N/A"
)

no2 = data["data"]["iaqi"].get(
    "no2",
    {}
).get(
    "v",
    "N/A"
)

temperature = data["data"]["iaqi"].get(
    "t",
    {}
).get(
    "v",
    "N/A"
)

humidity = data["data"]["iaqi"].get(
    "h",
    {}
).get(
    "v",
    "N/A"
)

city = data["data"]["city"]["name"]

# ---------------- DISPLAY OUTPUT ----------------

print("\n------ AQI DATA ------")

print("City:", city)

print("AQI:", aqi)

print("PM2.5:", pm25)

print("PM10:", pm10)

print("NO2:", no2)

print("Temperature:", temperature)

print("Humidity:", humidity)
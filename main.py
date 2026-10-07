import json
import urllib.parse
import urllib.request
from dataclasses import dataclass

@dataclass
class WeatherData:
    city: str
    temperature: int
    country: str

def load_cities(filename):
    with open(filename, "r", encoding="utf-8") as file:
        cities = [line.strip() for line in file if line.strip()]

    return list(dict.fromkeys(cities))

def get_weather(city):
    try:
        encoded_city = urllib.parse.quote(city)
        url = f"https://wttr.in/{encoded_city}?format=j1"

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.load(response)

        temperature = int(data["current_condition"][0]["temp_C"])
        country = data["nearest_area"][0]["country"][0]["value"]

        return WeatherData(
            city=city,
            temperature=temperature,
            country=country
        )

    except Exception as error:
        print(f"Failed to get weather for {city}: {error}")
        return None

cities = load_cities("cities.txt")

weather_data = []

for city in cities:
    weather = get_weather(city)

    if weather is not None:
        weather_data.append(weather)
        print(f"{weather.city}, {weather.country} {weather.temperature:+d} °C")

print("\nStatistics by country:")

countries = {}

for weather in weather_data:
    if weather.country not in countries:
        countries[weather.country] = []

    countries[weather.country].append(weather.temperature)


for country, temperatures in countries.items():
    city_count = len(temperatures)
    average_temperature = sum(temperatures) / city_count
    min_temperature = min(temperatures)
    max_temperature = max(temperatures)

    print(
        f"{country} — {city_count} cities, "
        f"avg: {average_temperature:+.1f} °C, "
        f"min: {min_temperature:+d} °C, "
        f"max: {max_temperature:+d} °C"
    )
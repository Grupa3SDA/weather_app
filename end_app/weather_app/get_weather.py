import requests
from django.conf import settings


def get_weather_data(city_name):
    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={city_name}"
        f"&units=metric&appid={settings.WEATHER_API_KEY}"
    )

    response_weather = requests.get(weather_url)
    response_weather.raise_for_status()
    weather_data = response_weather.json()

    return weather_data


def get_forecast_data(latitude, longitude):
    forecast_url = (
        f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}"
        f"&units=metric&appid={settings.FORECAST_API_KEY}"
    )
    response_forecast = requests.get(forecast_url)
    response_forecast.raise_for_status()
    forecast_data = response_forecast.json()

    return forecast_data


def get_air_pollution_data(latitude, longitude):
    air_pollution_url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}"
        f"&appid={settings.AIR_POLLUTION_API_KEY}"
    )
    response_air_pollution = requests.get(air_pollution_url)
    response_air_pollution.raise_for_status()
    air_pollution_data = response_air_pollution.json()

    return air_pollution_data

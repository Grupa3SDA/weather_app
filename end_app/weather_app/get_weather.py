import requests
from django.conf import settings
from requests.exceptions import HTTPError

from .entities import WeatherData, ForecastData, AirPollutionData


def get_weather(city_name):
    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={city_name}"
        f"&units=metric&appid={settings.WEATHER_API_KEY}")

    try:
        response_weather = requests.get(weather_url)
        response_weather.raise_for_status()
        raw_weather_data = response_weather.json()
        weather_data = WeatherData.from_raw_weather_data(raw_weather_data)
        latitude = weather_data.latitude
        longitude = weather_data.longitude
        return weather_data, latitude, longitude, None

    except HTTPError as e:
        if e.response.status_code >= 500:
            error_message = "Błąd API, spróbuj ponownie później lub skontaktuj się z administratorem strony."
        elif e.response.status_code == 404:
            error_message = "Nie znaleziono miasta w bazie danych, sprawdź nazwę i spróbuj ponownie."
        else:
            error_message = {"error": str(e)}
        return None, None, None, error_message


def get_forecast(latitude, longitude):
    forecast_url = (
        f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}"
        f"&units=metric&appid={settings.FORECAST_API_KEY}")

    try:
        response_forecast = requests.get(forecast_url)
        response_forecast.raise_for_status()
        raw_forecast_data = response_forecast.json()
        forecast_data = ForecastData.from_raw_forecast_data(raw_forecast_data)
        return forecast_data, None

    except HTTPError as e:
        if e.response.status_code >= 500:
            error_message = "Błąd API, spróbuj ponownie później lub skontaktuj się z administratorem strony."
        elif e.response.status_code == 404:
            error_message = "Nie znaleziono miasta w bazie danych, sprawdź nazwę i spróbuj ponownie."
        else:
            error_message = {"error": str(e)}
        return None, error_message


def get_air_pollution(latitude, longitude):
    air_pollution_url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}"
        f"&appid={settings.AIR_POLLUTION_API_KEY}")

    try:
        response_air_pollution = requests.get(air_pollution_url)
        response_air_pollution.raise_for_status()
        raw_pollution_data = response_air_pollution.json()
        air_pollution_data = AirPollutionData.from_raw_air_pollution_data(raw_pollution_data)
        return air_pollution_data, None

    except HTTPError as e:
        if e.response.status_code >= 500:
            error_message = "Błąd API, spróbuj ponownie później lub skontaktuj się z administratorem strony."
        elif e.response.status_code == 404:
            error_message = "Nie znaleziono miasta w bazie danych, sprawdź nazwę i spróbuj ponownie."
        else:
            error_message = {"error": str(e)}
        return None, error_message

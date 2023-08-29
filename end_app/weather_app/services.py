import requests
from django.conf import settings

from .entities import WeatherData, ForecastData, AirPollutionData


class WeatherService:
    def __init__(self, city_name):
        self.city_name = city_name
        self.weather_data = None
        self.forecast_data = None
        self.air_pollution_data = None
        self.response_weather = None
        self.response_forecast = None
        self.response_air_pollution = None

    def get_weather(self):
        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={self.city_name}"
            f"&units=metric&appid={settings.WEATHER_API_KEY}")

        response_weather = requests.get(weather_url)
        response_weather.raise_for_status()
        self.response_weather = response_weather
        raw_weather_data = response_weather.json()
        self.weather_data = WeatherData.from_raw_weather_data(raw_weather_data)

    def get_forecast(self):
        if self.weather_data is None:
            self.get_weather()
        latitude = self.weather_data.latitude
        longitude = self.weather_data.longitude
        forecast_url = (
            f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}"
            f"&units=metric&appid={settings.FORECAST_API_KEY}")

        response_forecast = requests.get(forecast_url)
        response_forecast.raise_for_status()
        self.response_forecast = response_forecast
        raw_forecast_data = response_forecast.json()
        self.forecast_data = ForecastData.from_raw_forecast_data(raw_forecast_data)

    def get_air_pollution(self):
        if self.weather_data is None:
            self.get_weather()
        latitude = self.weather_data.latitude
        longitude = self.weather_data.longitude
        air_pollution_url = (
            f"https://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}"
            f"&appid={settings.AIR_POLLUTION_API_KEY}")

        response_air_pollution = requests.get(air_pollution_url)
        response_air_pollution.raise_for_status()
        self.response_air_pollution = response_air_pollution
        raw_pollution_data = response_air_pollution.json()
        self.air_pollution_data = AirPollutionData.from_raw_air_pollution_data(raw_pollution_data)

    def get_all_data(self):
        self.get_weather()
        self.get_forecast()
        self.get_air_pollution()

    def get_weather_and_foreacst(self):
        self.get_weather()
        self.get_forecast()

    def get_weather_and_air_pollution(self):
        self.get_weather()
        self.get_air_pollution()
